import boto3
from boto3.dynamodb.conditions import Key
import time
import datetime

dynamodb = boto3.resource("dynamodb")
time_eps=300

# def read_last_row():
    # table = dynamodb.Table("Airplanes")
    # response = table.query(KeyConditionExpression=Key('icao24').eq('icao24'))
    # return response['Items']
    
def list_airplanes():
    table = dynamodb.Table('AirplanesLast')
    response = table.scan()
    airplanes = []
    data = {
        'Latitude': [],
        'Longitude': [],
        'Heading':[],
        'ICAO': [],
    }
    for i in response['Items']:
        # print("I: ",i)
        diff=datetime.datetime.now().timestamp() - float(i['timestamp'])
        # print("SEKUNDY: ", diff)
        if diff < time_eps:
            data['Latitude'].append(float(i['latitude']))
            data['Longitude'].append(float(i['longitude']))
            data['ICAO'].append(str(i['ICAO24']))
            data['Heading'].append(float(i['heading']))
    return data


if __name__ == '__main__':
    print(list_airplanes())