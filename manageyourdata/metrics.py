import os
import pandas as pd
import matplotlib.pyplot as plt
from manageyourdata.utils import constants


def general_details(df: pd.DataFrame, file_name: str) -> dict:
    metrics = {}  # Dictionary to store dataframe general metrics.

    metrics["Archivo de datos"] = file_name
    metrics["Registros (filas)"] = str(df.shape[0])
    metrics["Campos (columnas)"] = str(df.shape[1])

    nulls = df.isnull().sum().sum()
    metrics["Valores nulos"] = f"{(nulls / df.size) * 100:.2f}% ({str(nulls)})"

    duplicated = df.duplicated().sum()
    metrics["Filas duplicadas"] = f"{(duplicated / df.size) * 100:.2f}% ({str(duplicated)})"

    return metrics


def fields_details(df: pd.DataFrame, file_name: str) -> list[dict]:
    fields = list(dict())  # List of dicctionaries to store fields details.

    for field in df.columns.to_list():
        # Usefull data collected.
        data_type = str(df[field].dtype)
        easy_type = constants.TIPO_DATO.get(data_type, "Desconocido")
        nulls = df[field].isnull().sum().sum()

        # Update the object with obtained details.
        fields.append(
            {"Nombre": field, 
             "Tipo de dato": f"{easy_type} ({data_type})", 
             "Valores únicos": str(df[field].nunique()), 
             "Valores nulos": f"{(nulls / len(df)) * 100:.2f}% ({str(nulls)})",
            }
        )
        
        # Create plots for each field.
        for graph in constants.GRAPH_MAPPING[data_type]:
            os.makedirs(f"images/{file_name}/{field}", exist_ok=True)
            save_plot(df, field, graph, f"images/{file_name}/{field}/{graph}.png")

    return fields


def save_plot(df: pd.DataFrame, field: str, plot_type: str, filename: str):
    """Genera y guarda un gráfico según el tipo seleccionado."""
    plt.figure(figsize=(6, 4))

    if plot_type == "hist":
        df[field].hist(bins=20, color="royalblue", edgecolor="black")
        plt.xlabel(field)
        plt.ylabel("Frecuencia")
        plt.title(f"Histograma de {field}")

    elif plot_type == "box":
        df.boxplot(column=[field])
        plt.title(f"Boxplot de {field}")

    elif plot_type == "scatter":
        num_cols = df.select_dtypes(include=["number"]).columns
        if len(num_cols) < 2:
            return
        plt.scatter(df[num_cols[0]], df[num_cols[1]], alpha=0.5, color="darkblue")
        plt.xlabel(num_cols[0])
        plt.ylabel(num_cols[1])
        plt.title(f"Dispersión: {num_cols[0]} vs {num_cols[1]}")

    elif plot_type == "line":
        df[field].plot(kind="line", color="royalblue")
        plt.xlabel("Índice")
        plt.ylabel(field)
        plt.title(f"Gráfico de Línea de {field}")

    elif plot_type == "bar":
        df[field].value_counts().plot(kind="bar", color="royalblue")
        plt.xlabel(field)
        plt.ylabel("Frecuencia")
        plt.title(f"Gráfico de Barras de {field}")

    elif plot_type == "pie":
        df[field].value_counts().plot(kind="pie", autopct="%1.1f%%", 
                                      startangle=90, colors=["royalblue", "lightblue"])
        plt.ylabel("")
        plt.title(f"Gráfico circular de {field}")

    plt.grid(True)
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
