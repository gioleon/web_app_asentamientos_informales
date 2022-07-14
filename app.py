# Importing libraries
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/diabetes.csv")

df['Insulin'] = df['Insulin'].replace(0, df['Insulin'].median)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],  meta_tags=[
           {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

app.title = "Diabetes CSV"

app.layout = dbc.Container(
    [html.H1(["Diabetes Features distributions"]),

     dbc.Row(
         children=[
             dbc.Col(
                 [
                     dbc.Label("Please select one feature"),
                     dcc.Dropdown(
                         id="variable",
                         options=[{"label": i, "value": i}
                                  for i in df.columns],
                         value="Pregnancies",
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
    if feature != "Outcome":
        fig = px.histogram(df, x=feature, opacity=0.8,
                           color_discrete_sequence=['indianred'])
    else:
        fig = px.bar(df[feature].value_counts())
        fig.update_xaxes(tickvals=[0, 1], ticktext=["Positive", "Negative"])
        fig.update_traces(marker_color='indianred', opacity=0.8)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
