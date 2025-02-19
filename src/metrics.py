import pandas as pd


def obtain_details(df: pd.DataFrame, file_name: str):
    metrics = {}

    metrics["Archivo de datos"] = file_name
    metrics["Registros (filas)"] = str(df.shape[0])
    metrics["Campos (columnas)"] = str(df.shape[1])

    return metrics

def obtain_columns(df: pd.DataFrame):
    return df.columns.to_list()