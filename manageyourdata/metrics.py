import pandas as pd


def obtain_details(df: pd.DataFrame, file_name: str) -> dict:
    metrics = {}
    metrics["Archivo de datos"] = file_name
    metrics["Registros (filas)"] = str(df.shape[0])
    metrics["Campos (columnas)"] = str(df.shape[1])
    metrics["Valores nulos"] = str(df.isnull().sum().sum())
    metrics["Filas duplicadas"] = str(df.duplicated().sum())

    return metrics

def obtain_columns(df: pd.DataFrame) -> list[str]:
    # metrics["Tipos de datos por columna"] = df.dtypes.astype(str).to_string()
    # metrics["Estadísticas descriptivas"] = df.describe().to_string()
    # metrics["Valores nulos por columna"] = df.isnull().sum().to_string()
    # metrics["Valores únicos por columna"] = df.nunique().to_string()
    return df.columns.to_list()