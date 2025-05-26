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

# Call FastAPI backend
route_options = requests.get("http://localhost:8000/api/params/route").json()
route_options = [d['route'] for d in route_options]
dir_options = requests.get("http://localhost:8000/api/params/dir").json()
dir_options = [d['dir'] for d in dir_options]

# JavaScript function to modify the dash-leaflet map data
draw_point=assign(
    """function(feature, latlng) {
        return L.circleMarker(latlng, {
            radius: 6,
            fillColor: "#3388ff",
            color: "#ffffff",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.9,
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
                                    className="map",
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
    
    response = requests.get("http://localhost:8000/api/spatial/params", params={"route": route, "dir":dir})
    geojson = response.json()
    return geojson
