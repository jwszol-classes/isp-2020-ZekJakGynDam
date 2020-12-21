from opensky_api import OpenSkyApi

def get_airplanes(username, password):
    poland_bbox = (49.0273953314, 54.8515359564, 14.0745211117,24.0299857927)
    api = OpenSkyApi(username, password)
    return api.get_states(bbox=poland_bbox)
