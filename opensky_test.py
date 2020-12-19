from opensky_api import OpenSkyApi
import json
import pprint
pp = pprint.PrettyPrinter(indent=1)

credentials_path = "credentials.json"
credentials = json.load(open(credentials_path, "r"))

username = credentials["opensky_api"]["username"]
password = credentials["opensky_api"]["password"]

api = OpenSkyApi(username, password)

poland_bbox = (49.0273953314, 54.8515359564, 14.0745211117,24.0299857927)
states = api.get_states(bbox=poland_bbox)
pp.pprint(states)

for s in states.states:
    pp.pprint(s)
    
print(len(states.states))
    
    
