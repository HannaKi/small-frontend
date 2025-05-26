import dash
import dash_bootstrap_components as dbc
from dash import html

# external_stylesheets for the UI layout
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title='Sample app',
    use_pages=True,
)

server = app.server  # for compatibility with hosting

nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Boxplot", active="exact", href="/")),
        # dbc.NavItem(dbc.NavLink("Slow Map", active="exact", href="/map")),
        dbc.NavItem(dbc.NavLink("Fancy Map", active="exact", href="/fastmap")),
        # dbc.NavItem(dbc.NavLink("Placeholder 2", active="exact", href="/testi")),
    ],
    pills=True,
    fill=True,
    className="border my-4",
)


app.layout = dbc.Container(
    [
        html.H1("Neat UI"),
        html.Hr(),
        nav,
        dash.page_container,
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
