import json
import base64
import reverse_geocode


def get_decoded_data(record):
    decoded_data = base64.b64decode(record["kinesis"]["data"]).decode("utf8")
    return decoded_data


def create_table_item(airplane_data, delimiter="|"):
    airplane_data_split = airplane_data.split(delimiter)
    # We can add more data here
    item = {
        "icao24":    airplane_data_split[0]
        "timestamp": airplane_data_split[1]
        "latitude":  airplane_data_split[2]
        "longitude": airplane_data_split[3]
        "heading":   airplane_data_split[4]
    }
    return item


def is_above_country(item, country="Poland"):
    latitude  = item["latitude"]
    longitude = item["longitude"]
    coordinates = ((latitude, longitude),)
    result = reverse_geocode.search(coordinates)
    
    if result[country]:
        return True
    else:
        return False


def add_record(item, table):
    table.put_item(Item=item)


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    airplane_table = dynamodb.Table('Airplanes')

    for record in event["Records"]:
        airplane_data = get_decoded_data(record)
        item          = create_table_item(airplane_data)

        if is_above_country(item) is False:
            continue

        add_record(item, airplane_table)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        "event":event
    }
