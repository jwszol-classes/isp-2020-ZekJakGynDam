import boto3
from boto3.dynamodb.conditions import Key
import time
import datetime

dynamodb = boto3.resource("dynamodb")
time_eps=39000

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
        'from': [],
        'to':[],
        'departure_time_plan':[],
        'departure_time_actual':[],
        'arrival_time_plan':[],
        'estimated_arrival_time_datetime':[],
        'delay':[]
    }
    for i in response['Items']:
        # print("I: ",i)
        timestamp = datetime.datetime.strptime(i['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        diff=datetime.datetime.now()- timestamp
        # print("SEKUNDY: ", diff.seconds)
        if diff.seconds < time_eps:
            data['Latitude'].append(float(i['latitude']))
            data['Longitude'].append(float(i['longitude']))
            data['ICAO'].append(str(i['ICAO24']))
            data['Heading'].append(float(i['heading']))
            #mogłem się pomylić w nazwach
            data['from'].append(str(i['from']))
            data['to'].append(str(i['to']))
            data['departure_time_plan'].append(str(i['departure_time_plan']))
            data['departure_time_actual'].append(str(i['departure_time_actual']))
            data['arrival_time_plan'].append(str(i['arrival_time_plan']))
            data['estimated_arrival_time_datetime'].append(str(i['estimated_arrival_time_datetime']))
            data['delay'].append(str(i['estimated_delay']))
            
    return data


if __name__ == '__main__':
    print(list_airplanes())