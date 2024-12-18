import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import numpy as np
import joblib
import os
import pandas as pd


def clean_data(data_name, output_file="/root/airflow/data/data_sucia_limpia.csv"):
    """
    Limpia un dataset sucio, asegurando que:
    1. Se eliminen filas con valores nulos.
    2. La columna 'Max_Speed' se convierta de mph a km/h.
    3. Las columnas se renombren de acuerdo con el siguiente mapeo:
       - 'Max_Speed' -> 'Speed_Limit'
       - 'Vehicle_Count' -> 'Number_of_Vehicles'
       - 'Alcohol_Level' -> 'Driver_Alcohol'
    4. Se guarde el dataset limpio en el archivo especificado por `output_file`.

    Parámetros:
    - data_name: Nombre del archivo de entrada (debe estar en la carpeta `/root/airflow/data`).
    - output_file: Ruta donde se guardará el archivo limpio.
    """
    pass


def check_and_join_data(output_file="/root/airflow/data/joined_data.csv"):
    """
    Combina dos datasets (`data_limpia.csv` y `data_sucia_limpia.csv`) en uno solo.
    1. Carga ambos datasets desde `/root/airflow/data`.
    2. Une los datasets (concatenación vertical).
    3. Guarda el dataset combinado en el archivo especificado por `output_file`.

    Parámetros:
    - output_file: Ruta donde se guardará el dataset combinado.
    """
    pass


def inference(
        input_file="/root/airflow/data/joined_data.csv", 
        model_file="/root/airflow/models/xgboost_pipeline.joblib", 
        output_file="/root/airflow/data/predictions.csv"
    ):
    """
    Genera predicciones utilizando un modelo previamente entrenado.
    1. Carga el dataset combinado desde `input_file`.
    2. Verifica la existencia del modelo preentrenado en `model_file`.
    3. Prepara los datos para la predicción, eliminando columnas irrelevantes.
    4. Genera predicciones con el modelo cargado.
    5. Guarda las predicciones en un archivo CSV especificado por `output_file`.

    Parámetros:
    - input_file: Ruta del archivo combinado para predicción.
    - model_file: Ruta del archivo del modelo preentrenado.
    - output_file: Ruta donde se guardarán las predicciones.
    """
    pass
