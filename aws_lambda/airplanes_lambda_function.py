from decimal import Decimal
import json
import base64
import reverse_geocode
import datetime
import boto3

import geographical_distance
import flight_radar
import sexagesimal_to_decimal_converter


def get_decoded_data(record):
    decoded_data = base64.b64decode(record["kinesis"]["data"]).decode("utf8")
    return decoded_data


def extract_data_opensky(airplane_data_opensky, delimiter="|"):
    airplane_data_split = airplane_data_opensky.split(delimiter)

    datetime_formated = timestamp2datetime(float(airplane_data_split[1]))

    # We can add more data here
    airplane_data_opensky = {
        "ICAO24":    airplane_data_split[0],
        "timestamp": Decimal(airplane_data_split[1]),
        "datetime":  datetime_formated,
        "latitude":  Decimal(airplane_data_split[2]),
        "longitude": Decimal(airplane_data_split[3]),
        "heading":   Decimal(airplane_data_split[4])
        "on_ground": json.loads(airplane_data_split[5].lower())
        "velocity":  Decimal(airplane_data_split[6])
    }
    return airplane_data_opensky


def timestamp2datetime(timestamp):
    datetime_ = datetime.datetime.fromtimestamp(timestamp)
    datetime_formated = datetime_.strftime('%Y-%m-%d %H:%M:%S.%f')
    return datetime_formated


def complete_data(airplane_data, airports_dict):

    if airplane_data["From"] in airports_dict.keys() and \
        airplane_data["To"] in airports_dict.keys()

        departure_time_plan_datetime = timestamp2datetime(airplane_data["Departure_time"])
        arrival_time_plan_datetime   = timestamp2datetime(airplane_data["Arrival_time"])
        duration_plan = airplane_data["Arrival_time"] - airplane_data["Departure_time"] # s

        departure_time_actual_datetime = timestamp2datetime(airplane_data["Actual_departure_time"])

        start_lat = airports_dict[airplane_data["From"]]["coordinates_decimal"]["latitude"]
        start_lon = airports_dict[airplane_data["From"]]["coordinates_decimal"]["longitude"]
        stop_lat  = airports_dict[airplane_data["To"]]["coordinates_decimal"]["latitude"]
        stop_lon  = airports_dict[airplane_data["To"]]["coordinates_decimal"]["longitude"]
        distance_between_airports = geographical_distance.haversine_formula(start_lat, start_lon, stop_lat, stop_lon) # m

        latitude  = airplane_data["latitude"]
        longitude = airplane_data["longitude"]
        distance_between_airplane_and_airports = geographical_distance.haversine_formula(latitude, longitude, stop_lat, stop_lon) # m

        if airplane_data["velocity"] is not None:
            estimated_arrival_time          = airplane_data["timestamp"] + distance_between_airplane_and_airports/airplane_data["velocity"]
            estimated_arrival_time_datetime = timestamp2datetime(estimated_arrival_time)
            estimated_delay                 = estimated_arrival_time_datetime - airplane_data["Arrival_time"] #s
        else:
            estimated_arrival_time          = "<velocity is None>"
            estimated_arrival_time_datetime = "<velocity is None>"
            estimated_delay                 = "<velocity is None>"
    else:
        departure_time_plan_datetime        = "<not from to Poland>"
        arrival_time_plan_datetime          = "<not from to Poland>"
        duration_plan                       = "<not from to Poland>"
        distance_between_airports           = "<not from to Poland>"
        estimated_arrival_time              = "<not from to Poland>"
        estimated_arrival_time_datetime     = "<not from to Poland>"
        estimated_delay                     = "<not from to Poland>"

    airplane_data["departure_time_plan_datetime"]    = departure_time_plan_datetime
    airplane_data["departure_time_actual_datetime"]  = departure_time_actual_datetime
    airplane_data["arrival_time_plan_datetime"]      = arrival_time_plan_datetime
    airplane_data["duration_plan"]                   = duration_plan
    airplane_data["distance_between_airports"]       = distance_between_airports
    airplane_data["estimated_arrival_time"]          = estimated_arrival_time
    airplane_data["estimated_arrival_time_datetime"] = estimated_arrival_time_datetime
    airplane_data["estimated_delay"]                 = estimated_delay


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

        # From Flightradar
        "from":                  airplane_data["From"],
        "to"                     airplane_data["To"],
        "departure_time_plan":   airplane_data["departure_time_plan_datetime"],
        "arrival_time_plan":     airplane_data["arrival_time_plan_datetime"],
        "duration_plan":         airplane_data["duration_plan"],
        "departure_time_actual": airplane_data["departure_time_actual_datetime"],
        "velocity":              airplane_data["velocity"],

        # Estimated
        "estimated_delay": airplane_data["estimated_delay"]
    }
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


def airplanes_lambda_handler(event, context):
    # TODO implement

    # Set configuration variables
    country = "Poland"
    data_delimiter = "|"
    airports_dict_path = "airports_poland.json"

    # Set DynamoDB variables
    dynamodb                   = boto3.resource("dynamodb")
    airplanes_historical_table = dynamodb.Table("AirplanesHistorical")
    airplanes_last_table       = dynamodb.Table("AirplanesLast")
    # airplanes_flights_table    = dynamodb.Table("AirplanesFlights")

    airports_dict = json.load(open(airports_dict_path, "r"))

    # Main loop for each record
    for record in event["Records"]:
        # Get and decode airplane data
        airplane_data_opensky_raw = get_decoded_data(record)
        airplane_data_opensky = extract_data_opensky(airplane_data_opensky_raw, delimiter)

        # Get data from flightradar
        icao24 = airplane_data.split(data_delimiter)
        airplane_data_flightradar = flight_radar.get_data_from_icao(icao24)

        # Create airplance data
        airplane_data = {**airplane_data_opensky, **airplane_data_flightradar} # merge two dicts

        # Check if airplane is above defined country
        if is_above_country(airplane_data, country) is False:
            print("Discarded", airplane_data["ICAO24"])
            continue

        # Get additional data
        airplane_data = complete_data(airplane_data, airports_dict)

        # Create items for tables
        item_for_airplanes_last = create_item_for_airplanes_last(airplane_data, data_delimiter)

        # Update DynamoDB tables
        add_record(item_for_airplanes_last, airplanes_last_table)
        add_record(item_for_airplanes_last, airplanes_historical_table)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        "event":event
    }
