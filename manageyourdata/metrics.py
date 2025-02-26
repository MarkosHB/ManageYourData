import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from manageyourdata.utils import constants


def general_details(df: pd.DataFrame, file_name: str) -> dict:
    metrics = {}  # Dictionary to store dataframe general metrics.

    metrics["Archivo de datos"] = file_name
    metrics["Registros (filas)"] = str(df.shape[0])
    metrics["Campos (columnas)"] = str(df.shape[1])

    nulls = df.isnull().sum()
    total_nulls = nulls.sum()
    metrics["Valores nulos"] = f"{(total_nulls / df.size) * 100:.2f}% ({str(total_nulls)})"

    duplicated = df.duplicated().sum()
    metrics["Filas duplicadas"] = f"{(duplicated / df.size) * 100:.2f}% ({str(duplicated)})"

    save_nulls_distribution(nulls, f"images/{file_name}/nulls_distribution.png")
    save_correlation_heatmap(df, f"images/{file_name}/correlation_heatmap.png")

    return metrics


def save_nulls_distribution(nulls: pd.Series, filename: str):
    """Genera y guarda un gráfico de distribución de valores nulos."""
    if nulls.sum() > 0:  # Si hay valores nulos, genera el gráfico.
        plt.figure(figsize=(8, 4))
        cols_with_nulls = nulls[nulls>0].sort_values(ascending=False)
        plt.bar(cols_with_nulls.index, cols_with_nulls.values, color="gray", edgecolor="black")
        plt.title("Distribución de Valores Nulos")
        plt.ylabel("Cantidad de valores nulos")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.savefig(filename, bbox_inches="tight")
        plt.close()


def save_correlation_heatmap(df: pd.DataFrame, filename: str):
    """Genera y guarda un heatmap de correlación para variables numéricas."""
    numeric_df = df.select_dtypes(include=["number"])
    # Only if more than one numeric column.
    if numeric_df.shape[1] > 1:  
        corr_matrix = numeric_df.corr(method="pearson")

        plt.figure(figsize=(8, 6))
        plt.imshow(corr_matrix, cmap="coolwarm", interpolation="nearest")
        plt.colorbar(label="Escala de Correlación")

        labels = numeric_df.columns
        plt.xticks(np.arange(len(labels)), labels, rotation=45, ha="right")
        plt.yticks(np.arange(len(labels)), labels)

        plt.title("Mapa de Correlación usando el método de Pearson")
        plt.savefig(filename, bbox_inches="tight")
        plt.close()


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
            save_field_plot(df, field, graph, f"images/{file_name}/{field}/{graph}.png")

    return fields


def save_field_plot(df: pd.DataFrame, field: str, plot_type: str, filename: str):
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
