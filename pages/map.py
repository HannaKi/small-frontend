import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import requests
from dash import Input, Output, callback, dcc, html

dash.register_page(
    __name__,
)

geojson_data = requests.get("http://localhost:8000/spatial").json()

route_options = sorted({f["properties"]["route"] for f in geojson_data["features"]})
route_dropdown_options = [{"label": region, "value": region} for region in route_options]

dir_options = sorted({f["properties"]["dir"] for f in geojson_data["features"]})
dir_dropdown_options = [{"label": region, "value": region} for region in dir_options]

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Reitti"),
                dcc.Dropdown(
                    id="route_dropdown",
                    options=route_options,
                    placeholder="Valitse reitti",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Suunta"),
                dcc.Dropdown(
                    id="direction_dropdown",
                    options=dir_options,
                    placeholder="Valitse suunta",
                ),
            ]
        ),
        html.Div([dbc.Label("Vuosi"), dcc.RangeSlider(id='year-slider', min=2010, max=2023, step=1, value=[2015, 2020], marks={str(year): str(year) for year in range(2010, 2024)})]),
    ],
    body=True,
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dl.Map(center=[60.2, 24.9], zoom=10, children=[dl.TileLayer(), dl.GeoJSON(id="geojson-layer")], style={"width": "100%", "height": "500px", "margin": "auto"})),
            ],
        ),
    ],
    fluid=True,
)


@callback(
    Output("geojson-layer", "data"),
    Input("route_dropdown", "value"),
    Input("direction_dropdown", "value"),
)
def update_map(route, dir):
    if not all([route, dir]):
        return None

    filtered = geojson_data["features"]
    if route:
        filtered = [f for f in filtered if f["properties"].get("route") == route]
    if dir:
        filtered = [f for f in filtered if f["properties"].get("dir") == dir]
    # filtered = [f for f in filtered if f["properties"].get("spd") <= 5]
    return {"type": "FeatureCollection", "features": filtered}
