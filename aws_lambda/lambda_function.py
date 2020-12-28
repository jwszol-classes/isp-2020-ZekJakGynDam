import json
import base64
import reverse_geocode
import datetime
import boto3


def get_decoded_data(record):
    decoded_data = base64.b64decode(record["kinesis"]["data"]).decode("utf8")
    return decoded_data


def timestamp2datetime(timestamp):
    datetime_ = datetime.datetime.fromtimestamp(timestamp)
    datetime_formated = datetime_.strftime('%Y-%m-%d %H:%M:%S.%f')
    return datetime_formated


def create_table_item(airplane_data, delimiter="|"):
    airplane_data_split = airplane_data.split(delimiter)

    datetime_formated = timestamp2datetime(float(airplane_data_split[1]))

    # We can add more data here
    item = {
        "icao24":    airplane_data_split[0],
        "timestamp": float(airplane_data_split[1]),
        "datetime":  datetime_formated,
        "latitude":  float(airplane_data_split[2]),
        "longitude": float(airplane_data_split[3]),
        "heading":   float(airplane_data_split[4])
    }
    return item


def is_above_country(item, country):
    latitude  = float(item["latitude"])
    longitude = float(item["longitude"])
    coordinates = (latitude, longitude),
    result = reverse_geocode.search(coordinates)
    
    if result[0]["country"] == country:
        return True
    else:
        return False


def add_record(item, table):
    table.put_item(Item=item)


def lambda_handler(event, context):
    # TODO implement

    # Set configuration variables
    country = "Poland"

    # Set DynamoDB variables
    dynamodb             = boto3.resource('dynamodb')
    airplane_table       = dynamodb.Table('Airplanes')
    airplaneICAO24_table = dynamodb.Table('AirplanesICAO24')

    # Main loop for each record
    for record in event["Records"]:
        # Get and decode airplane data
        airplane_data = get_decoded_data(record)

        # Create items for tables
        item = create_table_item(airplane_data)
        # print(item)

        # Check if airplane is above defined country
        if is_above_country(item, country) is False:
            print("Discarded", item)
            continue

        # Update DynamoDB tables
        add_record(item, airplane_table)
        add_record(item, airplaneICAO24_table)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        "event":event
    }
