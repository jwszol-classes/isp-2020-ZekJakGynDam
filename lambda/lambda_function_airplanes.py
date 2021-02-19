from decimal import Decimal
import json
import base64
import reverse_geocode
import datetime
from datetime import timezone
import boto3


def get_decoded_data(record):
    decoded_data = base64.b64decode(record["kinesis"]["data"]).decode("utf8")
    return decoded_data


def extract_data_opensky(airplane_data_opensky, delimiter="|"):
    airplane_data_split = airplane_data_opensky.split(delimiter)

    datetime_formated = timestamp2datetime(float(airplane_data_split[1]), False)

    # We can add more data here
    airplane_data_opensky = {
        "ICAO24":    airplane_data_split[0],
        "timestamp": Decimal(airplane_data_split[1]),
        "datetime":  datetime_formated,
        "latitude":  Decimal(airplane_data_split[2]),
        "longitude": Decimal(airplane_data_split[3]),
        "heading":   Decimal(airplane_data_split[4]),
        "on_ground": json.loads(airplane_data_split[5].lower()),
        "velocity":  Decimal(airplane_data_split[6])
    }
    return airplane_data_opensky


def timestamp2datetime(timestamp, debug=True):
    datetime_ = datetime.datetime.fromtimestamp(timestamp)
    datetime_formated = datetime_.replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
    return datetime_formated


def item_corrector(item):
    for key in item.keys():
        if type(item[key]) == type(0.2):
            item[key] = Decimal(str(item[key]))
    return item


def create_item_for_airplanes_last(airplane_data):
    # We can add more data here
    item = {
        # From Opensky
        "ICAO24":    airplane_data["ICAO24"],
        "timestamp": airplane_data["timestamp"],
        "datetime":  airplane_data["datetime"],
        "latitude":  airplane_data["latitude"],
        "longitude": airplane_data["longitude"],
        "heading":   airplane_data["heading"],
        "on_ground": airplane_data["on_ground"],
        "velocity":  airplane_data["velocity"]
    }
    
    item = item_corrector(item)
    
    return item


def is_above_country(airplane_data, country):
    latitude  = float(airplane_data["latitude"])
    longitude = float(airplane_data["longitude"])
    coordinates = (latitude, longitude),
    result = reverse_geocode.search(coordinates)
    
    if result[0]["country"] == country:
        return True
    else:
        return False


def add_record(item, table):
    table.put_item(Item=item)


def lambda_handler_airplanes(event, context):
    # TODO implement

    # Set configuration variables
    country = "Poland"
    data_delimiter = "|"

    # Set DynamoDB variables
    dynamodb                   = boto3.resource("dynamodb")
    airplanes_historical_table = dynamodb.Table("AirplanesHistorical")
    airplanes_last_table       = dynamodb.Table("AirplanesLast")

    # Main loop for each record
    for record in event["Records"]:
        # Get and decode airplane data
        airplane_data_opensky_raw = get_decoded_data(record)
        airplane_data_opensky = extract_data_opensky(airplane_data_opensky_raw, data_delimiter)

        # Check if airplane is above defined country
        if is_above_country(airplane_data_opensky, country) is False:
            print("Discarded", airplane_data_opensky["ICAO24"])
            continue

        # Create items for tables
        item_for_airplanes_last = create_item_for_airplanes_last(airplane_data_opensky)

        # Update DynamoDB tables
        add_record(item_for_airplanes_last, airplanes_last_table)
        add_record(item_for_airplanes_last, airplanes_historical_table)
        print("Saved item: ", item_for_airplanes_last)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        "event":event
    }
