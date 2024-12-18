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
     # Cargar el archivo
    file_path = f"/root/airflow/data/{data_name}"
    data = pd.read_csv(file_path)

    # 1. Eliminar filas con valores nulos
    data = data.dropna()

    # 2. Convertir 'Max_Speed' de mph a km/h (1 mph = 1.60934 km/h)
    if 'Max_Speed' in data.columns:
        data['Max_Speed'] = data['Max_Speed'] / 0.621371

    # 3. Renombrar las columnas
    rename_map = {
        'Max_Speed': 'Speed_Limit',
        'Vehicle_Count': 'Number_of_Vehicles',
        'Alcohol_Level': 'Driver_Alcohol'
    }
    data = data.rename(columns=rename_map)

    # 4. Guardar el dataset limpio
    data.to_csv(output_file, index=False)


def check_and_join_data(output_file="/root/airflow/data/joined_data.csv"):
    """
    Combina dos datasets (`data_limpia.csv` y `data_sucia_limpia.csv`) en uno solo.
    1. Carga ambos datasets desde `/root/airflow/data`.
    2. Une los datasets (concatenación vertical).
    3. Guarda el dataset combinado en el archivo especificado por `output_file`.

    Parámetros:
    - output_file: Ruta donde se guardará el dataset combinado.
    """
    # 0. Rutas de los archivos de entrada
    data_limpia_path = "/root/airflow/data/data_limpia.csv"
    data_sucia_limpia_path = "/root/airflow/data/data_sucia_limpia.csv"

    # 1. Cargar los datasets
    data_limpia = pd.read_csv(data_limpia_path)
    data_sucia_limpia = pd.read_csv(data_sucia_limpia_path)

    # 2. Unir los datasets (concatenación vertical)
    combined_data = pd.concat([data_limpia, data_sucia_limpia], ignore_index=True)

    # 3. Guardar el dataset combinado
    combined_data.to_csv(output_file, index=False)

def preprocess(df):

    """
    Prepara el dataframe para luego ser entrenado. En particular:
    - Imputa valores nulos
    - Genera features para aumentar la explicabilidad del modelo
    """

    df_proc = df.copy()

    # Imputar
    ## Weather
    weather_mode = df_proc["Weather"].mode().iloc[0]
    df_proc["Weather"] = df_proc["Weather"].fillna(weather_mode)

    ## Driver_Alcohol
    df_proc["Driver_Alcohol"] = df_proc["Driver_Alcohol"].fillna(0)

    ## Driver_Age
    age_mean = df_proc["Driver_Age"].mean()
    df_proc["Driver_Age"] = df_proc["Driver_Age"].fillna(age_mean)

    # Feature Engineering
    df_proc["Speed_Accident"] = df_proc["Speed_Limit"] * df_proc["Accident"]
    df_proc["Traffic_Norm"] = df_proc["Traffic_Density"] - df_proc["Traffic_Density"].mean()

    return df_proc

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
    # 1. Cargar el dataset combinado
    data = pd.read_csv(input_file)
    
    
    # 2.1 Verificar la existencia del archivo del modelo
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"El archivo del modelo '{model_file}' no existe.")
                                
    # 2.2 Cargar el modelo preentrenado
    model = joblib.load(model_file)

    # 3. Preparar los datos para predicción
    columnas_utiles=['Weather', 'Road_Type', 'Time_of_Day', 'Traffic_Density', 'Speed_Limit', 'Number_of_Vehicles', 'Driver_Alcohol', 'Accident_Severity', 
                     'Road_Condition', 'Vehicle_Type', 'Driver_Age', 'Driver_Experience', 'Road_Light_Condition', 'Accident']
    
    df = data[columnas_utiles]

    df_limpio = preprocess(df)

    # 4. Generar predicciones
    predictions = model.predict(df_limpio)

    # 5. Crear un DataFrame con las predicciones y guardar en un archivo CSV
    prediction_df = df_limpio.copy()
    prediction_df["Predictions"] = predictions
    prediction_df.to_csv(output_file, index=False)
