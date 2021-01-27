import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import plotly_express as px
import plotly.graph_objects as go
from opensky_api import OpenSkyApi
import numpy as np

import boto3
from boto3.dynamodb.conditions import Key
from query_dynamo import list_airplanes
import json
import pandas as pd

credentials_path = "credentials.json"
credentials = json.load(open(credentials_path, "r"))

access_token = credentials["mapbox"]["access_token"]



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
api = OpenSkyApi()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ])
)
allpoints = {'Lat':[],'Lon':[]}
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    ##tutaj nalezy zmienic na ciagniecie danych z AWS-a
    # fig = go.Figure()
    # state=api.get_states(bbox=(49.0273953314, 54.8515359564, 14.0745211117, 24.0299857927)).states

    # data = {
    #     'Latitude': [],
    #     'Longitude': [],
    #     'Heading':[],
    #     'ICAO': [],
    #     'Flight_from': [],
    #     'Flight_to':[],
    #     'Departure_time_(planned)':[],
    #     'Departure_time':[],
    #     'Arrival_time_(planned)':[],
    #     'Arrival_time_(estimated)':[],
    #     'Delay':[]
    # }

    # # # Zbieranie danych
    # for i in range(len(state)):
    #     data['Longitude'].append(state[i].longitude )
    #     data['Latitude'].append (state[i].latitude  )
    #     data['ICAO'].append(state[i].icao24)
    #     data['Heading'].append(0)
    #     data['Flight_from'].append('from')
    #     data['Flight_to'].append('to')
    #     data['Departure_time_(planned)'].append('departure plan')
    #     data['Departure_time'].append('departure_time_actual')
    #     data['Arrival_time_(planned)'].append('arrival_time_plan')
    #     data['Arrival_time_(estimated)'].append('estimated_arrival_time_datetime')
    #     data['Delay'].append('estimated_delay')

    data=list_airplanes()


    df = pd.DataFrame(data)
    fig = px.scatter_mapbox(df,lat= "Latitude",lon= "Longitude",
    hover_data=['ICAO', "Flight_from",'Flight_to','Departure_time_(planned)','Departure_time','Arrival_time_(planned)','Arrival_time_(estimated)','Delay'])
    fig.update_traces(marker=dict(color="Darkred", size=7))
    fig.add_trace(go.Scattermapbox(
        lon=allpoints['Lon'], 
        lat = allpoints['Lat'],
        mode='markers',
        marker=go.scattermapbox.Marker( size=5, color="rgb(100, 100, 100)", opacity=0.5)))
    allpoints['Lon']+=data['Longitude']
    allpoints['Lat']+=data['Latitude']
    print(len(allpoints['Lat']))
    fig.update_layout(height=1000,showlegend=False)
    fig.update_mapboxes(accesstoken=access_token,
     zoom=5.8,
     center=dict(lat=51.8,lon=21.1),
     uirevision=len(data), #To jest takie troche dziwne, ale coś mu trzeba podać, bo inaczej resetuje widok - len data w tym przypadku zawsze wynosi 3 i sie nie powinno zmieniac
     style='dark',
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)