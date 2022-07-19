# Importing libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

from prepare_data import graph_servicios_facturados, load_data
from default_graphics import default_servicios_facturas, graph_sector

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
                        placeholder = "All"
                     )
                ]),
                dcc.Graph(
                    id="pct_servicios_graph",
                    figure=default_servicios_facturas()
                )
        ])
    ]
)


@app.callback(
    Output(component_id="pct_servicios_graph", component_property="figure"),
    Input(component_id="pct_servicios_sector", component_property="value")
)
def servicios_facturas(sector):
    df_services = graph_servicios_facturados(sector)

    fig = make_subplots(
        rows = 1, cols = 2,
        subplot_titles = [
            "Porcentaje de servicios públicos",
            "Cantidad servicios públicos"
        ]
    )
    fig.add_bar(
        x = df_services.columns,
        y = (df_services.sum(axis = 0)/df_services.shape[0]).values,
        row = 1, col = 1
    )

    fig.add_bar(
        x = df_services.drop("ninguno", axis=1).sum(axis=1).value_counts().index,
        y = df_services.drop("ninguno", axis=1).sum(axis=1).value_counts().values,
        row = 1, col = 2
    )

    fig.update_layout(
        showlegend=False,
        title = go.layout.Title(
            text = "Servicios públicos presentes en asentamientos informales"
            + f" sector: {sector}<br>"
            + f"<sup><b>{df_services.shape[0]} registros</sup><b>"
        )
    )

    return fig





if __name__ == "__main__":
    app.run_server(debug=True)
