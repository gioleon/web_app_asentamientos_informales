import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings("ignore")


def load_data() -> pd.DataFrame:
    """
    This function read the csv file
    and returns a dataframe object only
    wuith the columns of interest

    @return: pandas dataframe object.
    """
    cols = [
        "nombre del sector a caracterizar",
        "codigo de la vivienda",
        "cuantos pisos tiene la vivienda?",
        "tipo de vivienda",
        "¿durante la noche # espacios de la vivienda"
        + " se emplean como dormitorios",
        "estado general de la vivienda",
        "de que servicios públicos recibe factura?",
        'el servicio de acueducto llega a su vivienda las 24 horas al dia',
        'el servicio de energia llega a su vivienda las 24 horas al dia d',
        "responsable del hogar: genero",
        "responsable del hogar: ¿tiene diploma de alguno de los "
        + "siguiente niveles de escolaridad?",
        'cuantos hogares habitan esta vivienda?'
    ]

    df = pd.read_csv(

        "data/Censo_de_asentamientos_informales_Cartagena_2021.csv",
        encoding = "UTF-8"
    )

    df = df.rename(lambda x : str(x).lower(), axis = 1)
    df = df[cols].drop_duplicates()

    return  df


def rename_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function renames the columns
    of the dataframe.
    """
    cols_to_rename = [
        "sector",
        "codigo_vivienda",
        "n_pisos",
        "tipo_vivienda",
        "n_espacio_dormitorios_noche",
        "general_vivienda",
        "servicios_facturas",
        "acueducto_24/7",
        'energia_24/7',
        "genero_responsable",
        "diplomas_responsable",
        'n_hogares_vivienda'
    ]

    df.columns = cols_to_rename

    return df


df = rename_cols(load_data())
df.shape


def graph_servicios_facturados(sector = "all"):
    """
    This function will return a graphic of the
    bill services that each house receive.
    """
    if sector == "all":
        servicios_facturas = df.servicios_facturas.apply(str.lower)
    else:
        servicios_facturas = df["servicios_facturas"][
            df["sector"] == sector
        ].apply(str.lower)

    index_cols = servicios_facturas.apply(
        lambda x: len(x.split())
    ).sort_values().index[-1]

    cols = servicios_facturas.loc[index_cols].split(maxsplit = 5)

    df_servicios = pd.DataFrame(
        columns = cols + ["ninguno"],
        index = servicios_facturas.index
    )

    dict_temp = {}
    for i in range(servicios_facturas.shape[0]):
        dict_temp[df.codigo_vivienda.iloc[i]] = np.array(
            pd.Series(cols+["ninguno"]).isin(
                servicios_facturas.iloc[i].split(maxsplit=5)
            )
        )*1

    services_df = pd.DataFrame.from_dict(
        dict_temp,
        orient = "index",
        columns = cols + ["ninguno"]
    )

    return services_df


graph_servicios_facturados().sum(axis = 0)
