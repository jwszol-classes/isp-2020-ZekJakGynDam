import requests
import pprint
pp = pprint.PrettyPrinter(indent=1)
import json




api_access_key_path = "api_access_key.json"
api_access_key = json.load(open(api_access_key_path, "r"))
# print(params)

params = {
    'access_key': api_access_key["access_key"]
}


#api_result = requests.get('http://api.aviationstack.com/v1/countries', params)
#api_result = requests.get('http://api.aviationstack.com/v1/airlines', params)
#api_result = requests.get('http://api.aviationstack.com/v1/airports', params)
api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

api_response = api_result.json()
pp.pprint(api_response)

# for flight in api_response['data']:
#     if (flight['live']['is_ground'] is False):
#         print(u'%s flight %s from %s (%s) to %s (%s) is in the air.' % (
#             flight['airline']['name'],
#             flight['flight']['iata'],
#             flight['departure']['airport'],
#             flight['departure']['iata'],
#             flight['arrival']['airport'],
#             flight['arrival']['iata']))