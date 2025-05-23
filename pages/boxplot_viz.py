import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import requests
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')


# Call FastAPI backend
response = requests.get("http://localhost:8000/data")
data = response.json()
df = pd.DataFrame(data)


controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Reitti"),
                dcc.Dropdown(
                    id="route",
                    options=[{'label': x, 'value': x} for x in df["route"].unique()],
                    placeholder="Valitse reitti",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Suunta"),
                dcc.Dropdown(
                    id="direction",
                    options=[{'label': x, 'value': x} for x in df["dir"].unique()],
                    placeholder="Valitse suunta",
                ),
            ]
        ),
    ],
    body=True,
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="box-graph"), md=8),
            ],
        ),
    ],
    fluid=True,
)


@callback(
    Output("box-graph", "figure"),
    Input("route", "value"),
    Input("direction", "value"),
)
def make_graph(route, direction):

    dff = df[df["route"] == route]
    dff = dff[dff["dir"] == direction]
    # dff=dff.dropna(subset=["stop"], axis= 1)
    dff["stop"] = dff['stop'].astype(str)

    fig = px.box(dff, x="stop", y="dl")

    return fig
