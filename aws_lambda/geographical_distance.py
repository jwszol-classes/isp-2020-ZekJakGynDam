import numpy as np


def haversine_formula(lat1, lon1, lat2, lon2):
    R = 6371000                             # earth radius

    fi1 = lat1*np.pi/180
    fi2 = lat2*np.pi/180
    delta_fi     = (lat1-lat2)*np.pi/180
    delta_lambda = (lon1-lon2)*np.pi/180

    a = np.sin(delta_fi/2)*np.sin(delta_fi/2) + \
        np.cos(fi1)*np.cos(fi2) * \
        np.sin(delta_lambda/2)*np.sin(delta_lambda/2)

    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1-a))

    d = R*c

    return d


if __name__ == "__main__":
    lat1 = 54.8515359564
    lat2 = 49.0273953314
    lon1 = 0
    lon2 = 0
    d = haversine_formula(lat1, lon1, lat2, lon2)
    print(d)