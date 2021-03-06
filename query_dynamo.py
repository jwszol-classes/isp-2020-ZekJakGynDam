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
        'latitude': [],
        'longitude': [],
        'heading':[],
        'icao24': [],
        'velocity': [],
        'on_ground': [],
    }
    for i in response['Items']:
        # print("I: ",i)
        diff=datetime.datetime.now().timestamp() - float(i['timestamp'])
        # print("SEKUNDY: ", diff)
        if diff < time_eps:
            data['latitude'].append(float(i['latitude']))
            data['longitude'].append(float(i['longitude']))
            data['icao24'].append(str(i['ICAO24']))
            data['heading'].append(float(i['heading']))
            data['velocity'].append(float(i['velocity']))
            data['on_ground'].append(str(i['on_ground']))
    return data


if __name__ == '__main__':
    print(list_airplanes())