# Importing libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

from prepare_data import graph_servicios_facturados, load_data
from default_graphics import servicios_facturas, graph_sector, graph_n_pisos

df = load_data() # complete dataframe

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],  meta_tags=[
           {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

app.title = "Asentamientos informales"

app.layout = dbc.Container(
    [
        html.H1(["Analísis Asentamientos Informales"]),
        dbc.Row(
            dcc.Graph(
                id="sectores",
                figure=graph_sector()
            ),
        ),
        dbc.Row(
            children=[
                dbc.Col(
                [
                    dbc.Label("Seleccione un sector"),
                    dcc.Dropdown(
                        id="pct_servicios_sector",
                        options=[{"label": i, "value": i}
                                  for i in df.sector.unique()],
                        value="all",
                        placeholder = "All",
                        style={"width": "85%"}
                     )
                ]),
                dcc.Graph(
                    id="pct_servicios_graph",
                    figure=servicios_facturas()
                )
        ]),
        dbc.Row(
            dcc.Graph(
                id="graph_pisos",
                figure=graph_n_pisos()
            ),
        )
    ]
)


@app.callback(
    Output(component_id="pct_servicios_graph", component_property="figure"),
    Input(component_id="pct_servicios_sector", component_property="value")
)
def graph_servicios_facturas(sector):
    return servicios_facturas(sector)


@app.callback(
    Output(component_id="graph_pisos", component_property="figure"),
    Input(component_id="pct_servicios_sector", component_property="value")
)
def n_pisos(sector):
    return graph_n_pisos(sector)



if __name__ == "__main__":
    app.run_server(debug=True)
