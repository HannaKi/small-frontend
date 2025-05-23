# How to send dropdown vals to backend and filter data there?

import dash
from dash import dcc, html, Input, Output, callback
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import requests
from dash_extensions.javascript import assign


dash.register_page(
    __name__,
)

geojson_data = requests.get("http://localhost:8000/spatial").json()

route_options = sorted({f["properties"]["route"] for f in geojson_data["features"]})
route_dropdown_options = [{"label": region, "value": region} for region in route_options]

dir_options = sorted({f["properties"]["dir"] for f in geojson_data["features"]})
dir_dropdown_options = [{"label": region, "value": region} for region in dir_options]

# JavaScript function to modify the dash-leaflet map
draw_point=assign(
    """function(feature, latlng) {
        return L.circleMarker(latlng, {
            radius: 6,
            fillColor: "#3388ff",
            color: "#fff",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.9
            });
        }
    """)

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
    ],
    body=True,
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dl.Map(
                               
                               zoom=10, center=[60.2, 24.9], 
                               children=
                                    [
                                        dl.TileLayer(), 
                                        dl.GeoJSON(
                                            id="geojson-layer-fast", 
                                            zoomToBounds=True,
                                            pointToLayer=draw_point,
                                            )
                                    ], 
                                style={"width": "100%", "height": "500px", "margin": "auto"}
                        )
                ),
            ],
        ),
    ],
    fluid=True,
)


@callback(
    Output("geojson-layer-fast", "data"),
    Input("route_dropdown", "value"),
    Input("direction_dropdown", "value"),
)
def update_map(route, dir):
    if not all([route, dir]):
        return None
    
    response = requests.get("http://localhost:8000/spatial/params", params={"route": route, "dir":dir})
    geojson = response.json()
    return geojson
