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


fig = go.Figure()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
api = OpenSkyApi()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=2*1000, # in milliseconds
            n_intervals=0
        )
    ])
)
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    ##tutaj nalezy zmienic na ciagniecie danych z AWS-a
    # res = list_airplanes()
    # print(res)  
    # state=api.get_states(bbox=(49.0273953314, 54.8515359564, 14.0745211117, 24.0299857927)).states

    # data = {
    #     'Latitude': [],
    #     'Longitude': [],
    #     'ICAO': []
    # }

    # # Zbieranie danych
    # for i in range(len(state)):
    #     data['Longitude'].append(state[i].longitude )
    #     data['Latitude'].append (state[i].latitude  )
    #     data['ICAO'].append(state[i].icao24)
    data=list_airplanes()
    fig.update_traces(marker=go.scattermapbox.Marker( size=5, color="rgb(100, 100, 100)", opacity=0.0),mode='markers')#chamskie ale zamalowuje wszystkie stare punkty na szaro

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
        text=data['ICAO'],
        # label_bgcolor='rgb(200,200,200)',
        hoverinfo='text',
    ))


    fig.update_layout(height=1000,showlegend=False)
    fig.update_mapboxes(accesstoken="pk.eyJ1IjoiZGFhYW1pYW4iLCJhIjoiY2tqOHFnemZmNTB2eTJxc2NwbDR6bzNkciJ9.nPJVeE3p8ooX4vLrk9IMww",
     zoom=5.8,
     center=dict(lat=51.8,lon=21.1),
     uirevision=len(data), #To jest takie troche dziwne, ale coś mu trzeba podać, bo inaczej resetuje widok - len data w tym przypadku zawsze wynosi 3 i sie nie powinno zmieniac
     style='dark',
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
