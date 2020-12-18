from opensky_api import OpenSkyApi
import json
import pprint
pp = pprint.PrettyPrinter(indent=1)

credentials_path = "credentials.json"
credentials = json.load(open(credentials_path, "r"))

username = credentials["username"]
password = credentials["password"]

api = OpenSkyApi(username, password)
states = api.get_states()
pp.pprint(states)

for s in states.states:
    pp.pprint(s)
    
print(len(states.states))
    
    
