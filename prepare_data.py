import pandas as pd


def load_data() -> pd.DataFrame:
    """
    This function read the csv file
    and returns a dataframe object

    @return: pandas dataframe object
    """
    df = pd.read_csv(
        "data/Censo_de_asentamientos_informales_Cartagena_2021.csv",
        encoding = "UTF-8"
    )

    return df

print(load_data().head(5))
