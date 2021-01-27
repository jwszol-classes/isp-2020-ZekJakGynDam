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
            interval=15*1000, # in milliseconds
            n_intervals=0
        )
    ])
)
allpoints = {'Lat':[],'Lon':[]}
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    ##tutaj nalezy zmienic na ciagniecie danych z AWS-a
    # print(res)  
    fig = go.Figure()
    # state=api.get_states(bbox=(49.0273953314, 54.8515359564, 14.0745211117, 24.0299857927)).states

    # data = {
    #     'Latitude': [],
    #     'Longitude': [],
    #     'ICAO': []
    # }

    # # # Zbieranie danych
    # for i in range(len(state)):
    #     data['Longitude'].append(state[i].longitude )
    #     data['Latitude'].append (state[i].latitude  )
    #     data['ICAO'].append(state[i].icao24)
    data=list_airplanes()

    fig.add_trace(go.Scattermapbox(
        lon=allpoints['Lon'], 
        lat = allpoints['Lat'],
        mode='markers',
        marker=go.scattermapbox.Marker( size=5, color="rgb(100, 100, 100)", opacity=0.5)))
    allpoints['Lon']+=data['Longitude']
    allpoints['Lat']+=data['Latitude']
    print(len(allpoints['Lat']))
    texts = str(data['ICAO'])+'\n'+ \
            str(data['from'])+'\n'+ \
            str(data['to'])+'\n'+ \
            str(data['departura_time_plan'])+'\n'+ \
            str(data['departure_time_actual'])+'\n'+ \
            str(data['arrival_time_plan'])+'\n'+ \
            str(data['estimated_arrival_time_datetime'])+'\n'+ \
            str(data['delay'])+'\n'
    
    fig.add_trace(go.Scattermapbox(
        #name="Plane",
        lon=data['Longitude'],
        lat=data['Latitude'],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=10,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
        text=texts,
        # label_bgcolor='rgb(200,200,200)',
        hoverinfo='text',
    ))
    # print(fig.data)
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
