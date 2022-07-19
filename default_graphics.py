import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from prepare_data import graph_servicios_facturados, load_data


def graph_sector():
    df = load_data()
    df["x"] = [np.random.choice(np.arange(5)) for _ in range(df.shape[0])]
    df["y"] = [np.random.choice(np.arange(5)) for _ in range(df.shape[0])]

    df_grouped = df.groupby("sector")[["x", "y"]].sum().reset_index()
    df_grouped["numero viviendas"] = df.sector.value_counts().values

    fig = px.scatter(
        df_grouped, x = "x",
        y = "y", size = "numero viviendas",
        hover_name = "sector", color = "sector",
        hover_data = {
            "sector" : False,
            "numero viviendas" : True,
            "x" : False,
            "y" : False
        }
    )
    fig.update_layout(
        title = go.layout.Title(
            text = "Sectores con asentamientos informales<br>"
            + "<sup><b>el tamaño del punto es proporcional a la cantidad"
            + " de viviendas en dicho sector</b></sup>"
        )
    )
    fig.update_yaxes(title = "", showticklabels = False)
    fig.update_xaxes(title = "", showticklabels = False)

    return fig


def default_servicios_facturas():
    df_services = graph_servicios_facturados()

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
        row = 1, col = 1, name=""
    )

    fig.add_bar(
        x = df_services.drop("ninguno", axis=1).sum(axis=1).value_counts().index,
        y = df_services.drop("ninguno", axis=1).sum(axis=1).value_counts().values,
        row = 1, col = 2, name = ""
    )
    fig.update_traces(
        base="markers+lines"
    )
    fig.update_layout(
        showlegend = False,
        title = go.layout.Title(
            text = "Servicios públicos presentes en asentamientos informales"
            + " sector: Todos<br>"
            + f"<sup><b>{df_services.shape[0]} registros</sup></b><br>"
        )
    )

    return fig
