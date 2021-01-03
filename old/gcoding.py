import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import matplotlib.pyplot as plt
import plotly_express as px
from tqdm.notebook import tqdm_notebook

locator = Nominatim(user_agent="myGeocoder")

coordinates= "52.000, 11.000"
location =locator.reverse(coordinates)
print(location.raw)

url="https://www.dropbox.com/s/15gisj8hx218rn1/steet-pole-sample.csv?dl=1"
df=pd.read_csv(url)
df.head()
print(df)
# px.set_mapbox_access_token(open(".mapbox_token").read())
px.set_mapbox_access_token("pk.eyJ1IjoiZGFhYW1pYW4iLCJhIjoiY2tqOHFnemZmNTB2eTJxc2NwbDR6bzNkciJ9.nPJVeE3p8ooX4vLrk9IMww")
fig = px.scatter_mapbox(df,lat="Y",lon="X")
fig.show()