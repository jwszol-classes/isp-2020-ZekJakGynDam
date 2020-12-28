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
    for i in response['Items']:
        #print("I: ",i)
        timestamp = datetime.datetime.strptime(i['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        diff=datetime.datetime.now()- timestamp
        #print("SEKUNDY: ", diff.seconds)
        if diff.seconds < time_eps:
            airplanes.append(i) #i['icao24']
    return airplanes


# if __name__ == '__main__':
    # list_airplanes()