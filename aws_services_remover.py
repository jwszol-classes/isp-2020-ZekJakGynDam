# https://adamtheautomator.com/aws-lambda-python/?fbclid=IwAR3_6VJCZ3P1vYB6-6aVeXG40NCZL1rtPdzHCkFsY4K2CaG43AuEgRv0GCc#Creating_a_Lambda_Build_Function
# https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html

import boto3
import shutil
import os
import logging
import sys
from botocore.exceptions import ClientError
import json


def delete_kinesis_data_stream(aws_services_dict):
    client = boto3.client('kinesis')
    try:
        response = client.delete_stream(
            StreamName=aws_services_dict["Kinesis"]["stream_name"],
            EnforceConsumerDeletion=True
        )
        print(response)
    except ClientError as e:
        print("Kinesis data stream", aws_services_dict["Kinesis"]["stream_name"], "not exists and thus is not deleted")


def delete_dynamodb_tables(aws_services_dict):
    dynamodb = boto3.resource('dynamodb')
    for table in aws_services_dict["DynamoDB"]["tables"]:
        try:
            dynamodb_table = dynamodb.Table(table["TableName"])
            dynamodb_table.delete()
        except ClientError as e:
            print("DynamoDB table", table["TableName"], "not exists and thus is not deleted")


def delete_old_zip(zip_filename = "lambda/lambda.zip"):
    if os.path.exists(zip_filename):
        os.delete(zip_filename)
        print("The old file", zip_filename, "is deleted.")
    else:
        print("The file", zip_filename, "doesn't exists.")


def delete_s3_bucket(aws_services_dict):
    try:
        client = boto3.client('s3')
        client.delete_object(Bucket=aws_services_dict["S3"]["bucket_name"], 
                            Key=aws_services_dict["Lambda"]["Code"]["S3Key"])
    except ClientError as e:
        print("S3 bucket", aws_services_dict["S3"]["bucket_name"], "not exists and thus file", \
                aws_services_dict["Lambda"]["Code"]["S3Key"] ,"is not deleted")
   
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(aws_services_dict["S3"]["bucket_name"])
        bucket.delete()
    except ClientError as e:
        print("S3 bucket", aws_services_dict["S3"]["bucket_name"], "not exists and thus is not deleted")


def delete_lambda_function(aws_services_dict):
    client = boto3.client('lambda')
    try:
        response = client.delete_function(
            FunctionName=aws_services_dict["Lambda"]["FunctionName"],
        )
    except ClientError as e:
        print("Lambda function", aws_services_dict["Lambda"]["FunctionName"], "not exists and thus is not deleted")


def delete_iam(aws_services_dict):
    client = boto3.client('iam')

    for PolicyArn in aws_services_dict["IAM"]["policies_to_attach"]:
        try:
            response = client.detach_role_policy(
                RoleName=aws_services_dict["IAM"]["Lambda"]["RoleName"],
                PolicyArn=PolicyArn
            )
            print(response)
        except ClientError as e:
            print("IAM", aws_services_dict["IAM"]["Lambda"]["RoleName"], "not exists and thus policy ARN", PolicyArn, " is not detached")

    try:
        response = client.delete_role(
            RoleName=aws_services_dict["IAM"]["Lambda"]["RoleName"]
        )
        print(response)
    except ClientError as e:
        print("IAM", aws_services_dict["IAM"]["Lambda"]["RoleName"], "not exists and thus is not deleted")


def delete_policies(aws_services_dict):
    client = boto3.client('iam')
    for PolicyArn in aws_services_dict["IAM"]["policies_to_attach"]:
        if PolicyArn == "arn:aws:iam::aws:policy/AmazonKinesisFullAccess":
            continue
        else:
            try:
                response = client.delete_policy(PolicyArn=PolicyArn)
                print(response)
            except ClientError as e:
                print("policy ARN", PolicyArn, "not exists and thus is not deleted")


def delete_aws_services(aws_services_dict):
    # delete Kinesis data stream
    delete_kinesis_data_stream(aws_services_dict)

    # Prepare .zip file for Lambda
    delete_old_zip(aws_services_dict["Lambda"]["Code"]["S3Key"])

    # Create S3 bucket
    delete_s3_bucket(aws_services_dict)

    # delete iam
    delete_iam(aws_services_dict)

    # delete policies
    delete_policies(aws_services_dict)

    # Delete Lambda function
    delete_lambda_function(aws_services_dict)

    # Delete DynamoDB tables
    delete_dynamodb_tables(aws_services_dict)

    
if __name__ == "__main__":
    aws_services_dict = json.load(open('aws_services_config.json', 'r')) 
    delete_aws_services(aws_services_dict)