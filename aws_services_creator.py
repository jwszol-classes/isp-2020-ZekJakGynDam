# https://adamtheautomator.com/aws-lambda-python/?fbclid=IwAR3_6VJCZ3P1vYB6-6aVeXG40NCZL1rtPdzHCkFsY4K2CaG43AuEgRv0GCc#Creating_a_Lambda_Build_Function
# https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html

import boto3
import shutil
import os
import logging
import sys
from botocore.exceptions import ClientError
import json
import time


def create_kinesis_data_stream_airplanes(stream_name="kinesis_data_stream_airplanes", shard_count=2, region="us-east-1"):
    command = 'aws kinesis create-stream \
    --stream-name ' + str(stream_name) + ' \
    --shard-count ' + str(shard_count) + ' \
    --region ' + str(region)

    os.system(command)


def remove_old_zip(zip_filename = "lambda/lambda.zip"):
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        print("The old file", zip_filename, "is removed.")
    else:
        print("The file", zip_filename, "doesn't exists.")


def create_zip(zip_filename = "lambda/lambda"):
    if zip_filename[-4:] == ".zip":
        shutil.make_archive(zip_filename[:-4], 'zip', "lambda")
    else:
        shutil.make_archive(zip_filename, 'zip', "lambda")
    print("The new file", zip_filename, "is created.")


def create_bucket(bucket_name="s3bucketairplanes", region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def send_zip_file_to_S3(bucket_name="s3bucketairplanes", zip_filename="lambda/lambda.zip"):
    s3_client = boto3.resource('s3')
    s3_object = s3_client.Object(bucket_name, zip_filename)
    s3_object.upload_file(zip_filename)


def create_policy(PolicyName, PolicyDocument):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/iam-example-policies.html

    # Create IAM client
    iam = boto3.client('iam')
    try:
        response = iam.create_policy(
            PolicyName=PolicyName,
            PolicyDocument=str(PolicyDocument).replace("'", "\"")
        )
    except ClientError as e:
        logging.error(e)
        # print("Policy" , "\"" + PolicyName + "\" already exists and thus is not created.")


def create_policies(policies_list):
    for policy in policies_list:
        create_policy(policy["PolicyName"], policy["PolicyDocument"])


def create_iam(aws_services_dict):
    # https://stackoverflow.com/questions/44121532/how-to-create-aws-iam-role-attaching-managed-policy-only-using-boto3
    
    create_policies(aws_services_dict["IAM"]["policies_to_create"])

    client = boto3.client('iam')
    try:
        aws_services_dict_formatted = aws_services_dict["IAM"]["Lambda"]
        aws_services_dict_formatted["AssumeRolePolicyDocument"] = \
            str(aws_services_dict_formatted["AssumeRolePolicyDocument"]).replace("'", "\"")

        response = client.create_role(
            **aws_services_dict_formatted
        )
    except ClientError as e:
        logging.error(e)
        # print("IAM" , "\"" + aws_services_dict["IAM"]["Lambda"]["RoleName"] + "\" already exists and thus is not created.")

    for PolicyArn in aws_services_dict["IAM"]["policies_to_attach"]:
        response = client.attach_role_policy(
                RoleName=aws_services_dict["IAM"]["Lambda"]["RoleName"], 
                PolicyArn=PolicyArn
            )


def create_lambda_function(aws_services_dict):
    client = boto3.client('lambda')
    try:
        create_lambda_function = client.create_function(
            **aws_services_dict["Lambda"]
        )
    except ClientError as e:
        logging.error(e)
    #     print("Lambda function", aws_services_dict["Lambda"]["FunctionName"], "already exists and thus isn't created")


def create_event_source_mapping(aws_services_dict):
    client = boto3.client('lambda')
    try:
        response = client.create_event_source_mapping(
            **aws_services_dict["Lambda_source_mapping"]["create"]
        )
        print(response)

        aws_services_dict["Lambda_source_mapping"]["delete"]["UUID"] = response["UUID"]
        json.dump(aws_services_dict, open('aws_services_config.json', 'w'), indent=4)
    except ClientError as e:
        logging.error(e)

        aws_services_dict["Lambda_source_mapping"]["delete"]["UUID"] = str(e).split(" UUID ")[1]
        json.dump(aws_services_dict, open('aws_services_config.json', 'w'), indent=4)


def create_table(table):
    dynamodb_client = boto3.client('dynamodb')
    try:
        table1 = dynamodb_client.create_table(
            **table
        )
        print(table["TableName"], "status:", table1)
    except ClientError as e:
        logging.error(e)
        # print("Table", table["TableName"], "already exists and thus isn't created")


def create_dynamodb_tables(aws_services_dict):
    for table in aws_services_dict["DynamoDB"]["tables"]:
        create_table(table)


def create_aws_services(aws_services_dict):
    # Create Kinesis data stream
    create_kinesis_data_stream_airplanes(**aws_services_dict["Kinesis"])

    # Prepare .zip file for Lambda
    remove_old_zip(aws_services_dict["Lambda"]["Code"]["S3Key"])
    create_zip(aws_services_dict["Lambda"]["Code"]["S3Key"])

    # Create S3 bucket
    create_bucket(**aws_services_dict["S3"])

    # Send .zip file on S3 bucket
    send_zip_file_to_S3(aws_services_dict["S3"]["bucket_name"], aws_services_dict["Lambda"]["Code"]["S3Key"])

    # Create IAM for Lambda
    create_iam(aws_services_dict)

    # For some reason we need to wait some time between creating role and creating lambda function
    time.sleep(10)

    # Create Lambda function
    create_lambda_function(aws_services_dict)

    # Create Lambda function
    create_event_source_mapping(aws_services_dict)

    # Create DynamoDB tables
    create_dynamodb_tables(aws_services_dict)

    
if __name__ == "__main__":
    aws_services_dict = json.load(open('aws_services_config.json', 'r')) 
    create_aws_services(aws_services_dict)