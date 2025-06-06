import dash
from dash import dcc, html, Input, Output, callback

dash.register_page(
    __name__,
)

layout = html.Div(
    [
        dcc.Dropdown(id='dropdown-to-show_or_hide-element', options=[{'label': 'Show element', 'value': 'on'}, {'label': 'Hide element', 'value': 'off'}], value='on'),
        # Create Div to place a conditionally visible element inside
        html.Div(
            [
                # Create element to hide/show, in this case an 'Input Component'
                dcc.Input(
                    id='element-to-hide',
                    placeholder='something',
                    value='Can you see me?',
                )
            ],
            style={'display': 'block'},  # <-- This is the line that will be changed by the dropdown callback
        ),
    ]
)


@callback(Output(component_id='element-to-hide', component_property='style'), [Input(component_id='dropdown-to-show_or_hide-element', component_property='value')])
def show_hide_element(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}
