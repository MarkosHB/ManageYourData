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

    # Generate associated plots.
    os.makedirs(f"images/{file_name}", exist_ok=True)
    save_field_types(df, f"images/{file_name}/field_types.png")
    save_nulls_distribution(nulls, f"images/{file_name}/nulls_distribution.png")
    save_correlation_heatmap(df, f"images/{file_name}/correlation_heatmap.png")

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
             "Valores nulos": f"La proporción de instancias vacías es de un {(nulls / len(df)) * 100:.2f}% ({str(nulls)})",
             "Valores únicos": f"Existen {str(df[field].nunique())} instancias diferentes para las {len(df)} entradas", 
             "Moda": f"La instancia más repetida es: {df[field].mode().values[0]}" if df[field].nunique() > 0 else "No existen valores únicos",
             "Mediana": f"La instancia central es: {df[field].median()}" if data_type == "int64" or data_type == "float64" else "No aplicable al tipo de datos",
             "Media": f"La instancia promedio es: {df[field].mean().round(2)}" if data_type == "int64" or data_type == "float64" else "No aplicable al tipo de datos",
             "DE": f"La desviación estándar es: {df[field].std().round(2)}" if data_type == "int64" or data_type == "float64" else "No aplicable al tipo de datos",
            }
        )

        # Create plots for each field.
        for graph in constants.GRAPH_MAPPING[data_type]:
            os.makedirs(f"images/{file_name}/{field}", exist_ok=True)
            save_field_plot(df, field, graph, f"images/{file_name}/{field}/{graph}.png")

    return fields


def save_field_types(df: pd.DataFrame, file_path: str):
    """Genera y guarda un gráfico de tipos de datos de las columnas."""
    types = df.dtypes.value_counts().sort_values(ascending=False)
    plt.figure(figsize=(6, 4))
    plt.bar(types.index.astype(str), types.values, color="green", edgecolor="black")
    plt.title("Distribución de Tipos de Datos")
    plt.ylabel("Total de columnas")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.savefig(file_path, bbox_inches="tight")
    plt.close()


def save_nulls_distribution(nulls: pd.Series, file_path: str):
    """Genera y guarda un gráfico de distribución de valores nulos."""
    if nulls.sum() > 0:  # Si hay valores nulos, genera el gráfico.
        plt.figure(figsize=(8, 4))
        cols_with_nulls = nulls[nulls>0].sort_values(ascending=False)
        plt.bar(cols_with_nulls.index, cols_with_nulls.values, color="gray", edgecolor="black")
        plt.title("Distribución de Valores Nulos")
        plt.ylabel("Cantidad de valores nulos")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.savefig(file_path, bbox_inches="tight")
        plt.close()


def save_correlation_heatmap(df: pd.DataFrame, file_path: str):
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
        plt.savefig(file_path, bbox_inches="tight")
        plt.close()


def save_field_plot(df: pd.DataFrame, field: str, plot_type: str, file_path: str):
    """Genera y guarda un gráfico según el tipo seleccionado."""
    plt.figure(figsize=(6, 4))
    # Hide labels if too many values.
    if df[field].nunique() > constants.MAX_LABELS: 
        show_vals = None
        info = None
    else: 
        show_vals = df[field].value_counts().index.tolist() 
        info = '%1.1f%%'

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
            return  # Do not generate.
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
        if show_vals is None: plt.xticks([])
        plt.xlabel(field)
        plt.ylabel("Frecuencia")
        plt.title(f"Gráfico de Barras de {field}")

    elif plot_type == "pie":
        df[field].value_counts().plot(kind="pie", labels=show_vals, autopct=info, startangle=90)
        plt.ylabel("")  # Not important.
        plt.title(f"Gráfico circular de {field}")

    plt.grid(True)
    plt.savefig(file_path, bbox_inches="tight")
    plt.close()
