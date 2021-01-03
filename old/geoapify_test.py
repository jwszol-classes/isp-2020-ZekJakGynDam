import requests
import pprint
pp = pprint.PrettyPrinter(indent=1)
import json


credentials_path = "credentials.json"
credentials = json.load(open(credentials_path, "r"))

params = {
    'lat': 54.8304419,
    'lon': 18.3044272,
    'apiKey': credentials["geoapify"]["apikey"]
}

api_result = requests.get("https://api.geoapify.com/v1/geocode/reverse", params)

api_response = api_result.json()
pp.pprint(api_response)

country = api_response["features"][0]["properties"]["country"]
print(country)