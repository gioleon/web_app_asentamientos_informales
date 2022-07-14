# Importing libraries
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],  meta_tags=[
           {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

app.title = "por definir"

app.layout = dbc.Container(
    [html.H1(["Diabetes Features distributions"]),

     dbc.Row(
         children=[
             dbc.Col(
                 [

                     )
                 ]),

             dcc.Graph(id="my-graph")
         ]
    )
    ]

)


@app.callback(
    Output(component_id="my-graph", component_property="figure"),
    Input(component_id="variable", component_property="value")
)
def make_graph(feature):
    pass


if __name__ == "__main__":
    app.run_server(debug=True)
