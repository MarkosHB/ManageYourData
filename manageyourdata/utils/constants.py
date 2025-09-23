# Currently accepted file format.
FORMAT = {"excel": ".xlsx", "csv": ".csv"}

# Model providers for llm agents.
MODEL_PROVIDERS = ["Ollama", "Google"]

# Pandas DataFrame data types.
TIPO_DATO = {
    "object": "Cadena de caracteres",
    "string": "Cadena de caracteres",
    "int64": "Número entero de 64 bits",
    "int32": "Número entero de 32 bits",
    "uint8": "Número entero sin signo de 8 bits",
    "uint16": "Número entero sin signo de 16 bits",
    "uint32": "Número entero sin signo de 32 bits",
    "uint64": "Número entero sin signo de 64 bits",
    "float64": "Número decimal de 64 bits",
    "float32": "Número decimal de 32 bits",
    "datetime64": "Fecha en formato YYYY-MM-DD",
    "timedelta64": "Diferencia entre fechas",
    "bool": "Booleano (Verdadero/Falso)",
    "category": "Categoría",
    "complex64": "Número complejo de 64 bits",
    "complex128": "Número complejo de 128 bits",
}

# Mapping of data types to suitable graphs.
GRAPH_MAPPING = {
    "int64": ["hist", "box"],
    "int32": ["hist", "box"],
    "uint8": ["hist", "box"],
    "uint16": ["hist", "box"],
    "uint32": ["hist", "box"],
    "uint64": ["hist", "box"],
    "float64": ["hist", "box"],
    "float32": ["hist", "box"],
    "bool": ["bar", "pie"],
    "object": ["bar", "pie"],
    "string": ["bar", "pie"],
    "category": ["bar", "pie"],
}

# Number of labels shown in plots.
MAX_LABELS = 10

# References.
GITHUB_URL = "https://github.com/MarkosHB/ManageYourData"