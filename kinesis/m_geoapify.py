import requests
import json

def get_country(params):
    api_result = requests.get("https://api.geoapify.com/v1/geocode/reverse", params)
    api_response = api_result.json()
    if len(api_response["features"])>0:
        return api_response["features"][0]["properties"]["country"]
    else:
        return "ERR"