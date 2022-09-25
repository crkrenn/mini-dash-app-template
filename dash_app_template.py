#######################
# notes
#######################

#######################
# python imports
#######################

# system
import json

# community
import pandas as pd

# plotly/dash
import dash
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# support for JupyterDash

def is_interactive():
    import __main__ as main
    return not hasattr(main, '__file__')

if is_interactive():
    print("interactive!")
    from jupyter_dash import JupyterDash

#######################
# Data Analysis / Model
#######################

df = px.data.stocks()

#########################
# Dashboard Layout / View
#########################

if is_interactive():
    app = JupyterDash()
else:
    app = dash.Dash()

app.layout = html.Div(
    id='parent',
    children=[
        html.H1(
            id='H1',
            children='Styling using html components',
            style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Google', 'value': 'GOOG'},
                {'label': 'Apple', 'value': 'AAPL'},
                {'label': 'Amazon', 'value': 'AMZN'},
                ],
            value='GOOG'),
        dcc.Graph(id='bar_plot')
    ])

#############################################
# Interaction Between Components / Controller
#############################################


@app.callback(
    Output(component_id='bar_plot', component_property='figure'),
    [Input(component_id='dropdown', component_property='value')])

def graph_update(dropdown_value):
    print(dropdown_value)
    fig = go.Figure(
        [go.Scatter(
            x=df['date'],
            y=df['{}'.format(dropdown_value)],
            line=dict(color='firebrick', width=4))
        ])
    fig.update_layout(
        title='Stock prices over time',
        xaxis_title='Dates',
        yaxis_title='Prices'
    )
    return fig

if __name__ == '__main__':
    if is_interactive():
        app.run_server(mode='inline')
    else:
        app.run_server(debug=True, port=8893)
