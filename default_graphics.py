import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from prepare_data import graph_servicios_facturados, load_data


df = load_data()
colors = px.colors.qualitative.Pastel

def graph_sector():

    df_sector = load_data()

    df_sector["x"] = [
        np.random.choice(np.arange(5)) for _ in range(df_sector.shape[0])
    ]
    df_sector["y"] = [
        np.random.choice(np.arange(5)) for _ in range(df_sector.shape[0])
    ]

    df_sector_grouped = df_sector.groupby("sector")[["x", "y"]].sum().reset_index()
    df_sector_grouped["numero viviendas"] = df_sector.sector.value_counts().values

    fig = px.scatter(
        df_sector_grouped, x = "x",
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


def servicios_facturas(sector = "all"):
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
        row = 1, col = 1, name="",
        marker_color = [
            colors[i] for i in range(len(df_services.columns))
        ]
    )

    fig.add_bar(
        x = df_services.drop("ninguno", axis=1).sum(axis=1).value_counts().index,
        y = df_services.drop("ninguno", axis=1).sum(axis=1).value_counts().values,
        row = 1, col = 2, name = "",
        marker_color = [
            colors[i] for i in range(len(
                df_services.drop(
                    "ninguno", axis=1
                ).sum(axis=1).value_counts().index
            ))
        ]
    )
    fig.update_traces(
        base="markers+lines"
    )
    fig.update_layout(
        showlegend = False,
        title = go.layout.Title(
            text = "Servicios públicos presentes en asentamientos informales"
            + f" sector: {sector.capitalize()}<br>"
            + f"<sup><b>{df_services.shape[0]} registros</sup></b><br>"
        )
    )

    return fig


def graph_n_pisos(sector = "all"):

    if sector == "all":
        df_pisos = df[(df.n_pisos >= 1) & (df.n_pisos <= 4)]
    else:
        df_pisos = df[
            ((df.n_pisos >= 1) & (df.n_pisos <= 4))
            & (df["sector"]  == sector)
        ]

    df_pisos_count = df_pisos.n_pisos.value_counts()

    fig = make_subplots(
        rows = 1, cols = 2,
        specs =[[
            {"type": "pie"}, {"type": "bar"}
        ]]
    )

    fig.add_trace(
        go.Pie(
            values = df_pisos_count.values/df_pisos.shape[0],
            labels = df_pisos_count.index,
            marker_colors = [
                colors[i] for i in range(len(df_pisos_count.index))
            ]
        ),
        col = 1, row = 1
    )
    fig.add_trace(
        go.Bar(
            x = df_pisos_count.index,
            y = df_pisos_count.values,
            name = "",
            marker_color = [
                colors[i] for i in range(len(df_pisos_count.index))
            ]
        ),
        row = 1, col = 2
    )

    fig.update_layout(
        title = go.layout.Title(
            text = "Distribución del numero de pisos en asentamientos"
            + f" informales en el sector: {sector.capitalize()}"
        ),
        showlegend=False,
        margin=dict(t=100)
    )

    return fig
