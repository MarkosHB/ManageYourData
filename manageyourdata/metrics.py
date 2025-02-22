import pandas as pd


def general_details(df: pd.DataFrame, file_name: str) -> dict:
    metrics = {}  # Dictionary to store dataframe general metrics.
    metrics["Archivo de datos"] = file_name
    metrics["Registros (filas)"] = str(df.shape[0])
    metrics["Campos (columnas)"] = str(df.shape[1])
    metrics["Valores nulos"] = str(df.isnull().sum().sum())
    metrics["Filas duplicadas"] = str(df.duplicated().sum())

    return metrics


def fields_details(df: pd.DataFrame) -> list[dict]:
    fields = list(dict())  # List of dicctionaries to store fields details.
    for field in df.columns.to_list():
        fields.append(
            {"Nombre": field, 
             "Tipo de datos": str(df[field].dtype), 
             "Valores únicos": df[field].nunique(), 
             "Valores nulos": df[field].isnull().sum(),
            }
        )

    return fields
