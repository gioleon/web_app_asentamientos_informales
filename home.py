# Importing libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

from prepare_data import graph_servicios_facturados

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],  meta_tags=[
           {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

app.title = "por definir"

app.layout = dbc.Container(
    [html.H1(["Diabetes Features distributions"]),

     dbc.Row(
         children=[
             dbc.Col(
                 [
                    

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
def servicios_facturas():
    df = graph_servicios_facturados()

    fig = make_subplots(rows = 1, cols = 2)
    fig.add_trace(
        go.Pie(
            labels = df.sum(axis = 0)/df.shape[0].index,
            values = df.sum(axis = 0)/df.shape[0].values
        ),
        row = 1, col = 1
    )

    return fig





if __name__ == "__main__":
    app.run_server(debug=True)
