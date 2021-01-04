import boto3
from boto3.dynamodb.conditions import Key
import time
import datetime

dynamodb = boto3.resource("dynamodb")
time_eps=3

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
        # 'timestamp':[]
    }
    for i in response['Items']:
        # print("I: ",i)
        timestamp = datetime.datetime.strptime(i['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        diff=datetime.datetime.now()- timestamp
        # print("SEKUNDY: ", diff.seconds)
        if diff.seconds < time_eps:
            # airplanes.append(i) #i['icao24']
            data['Latitude'].append(float(i['latitude']))
            data['Longitude'].append(float(i['longitude']))
            data['ICAO'].append(str(i['ICAO24']))
            data['Heading'].append(float(i['heading']))
            
    return data


if __name__ == '__main__':
    print(list_airplanes())