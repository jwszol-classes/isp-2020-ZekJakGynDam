import boto3
from boto3.dynamodb.conditions import Key
import time
import datetime

dynamodb = boto3.resource("dynamodb")
time_eps=390000

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
        'Flight_from': [],
        'Flight_to':[],
        'Departure_time_(planned)':[],
        'Departure_time':[],
        'Arrival_time_(planned)':[],
        'Arrival_time_(estimated)':[],
        'Delay':[]
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
            data['Flight_from'].append(str(i['from']))
            data['Flight_to'].append(str(i['to']))
            data['Departure_time_(planned)'].append(str(i['departure_time_plan']))
            data['Departure_time'].append(str(i['departure_time_actual']))
            data['Arrival_time_(planned)'].append(str(i['arrival_time_plan']))
            data['Arrival_time_(estimated)'].append(str(i['estimated_arrival_time_datetime']))
            data['Delay'].append(str(i['estimated_delay']))
            
    return data


if __name__ == '__main__':
    print(list_airplanes())