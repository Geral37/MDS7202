import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
import joblib
import gradio as gr

# 1. create_folders()
def create_folders(**kwargs):
    """
    Crea una carpeta con la fecha de ejecución del DAG como nombre y las subcarpetas: raw, splits, models.
    """
    # Obtener execution_date desde kwargs
    execution_date_str = kwargs.get("execution_date", datetime.now().strftime('%Y-%m-%d'))
    execution_date = datetime.strptime(execution_date_str, "%Y-%m-%d")

    base_folder = f"dags/{execution_date.strftime('%Y-%m-%d')}"
    subfolders = ["raw", "splits", "models"]

    # Crear las carpetas
    for subfolder in subfolders:
        os.makedirs(os.path.join(base_folder, subfolder), exist_ok=True)

    print(f"Carpetas creadas en: {base_folder}")

# 2. split_data()
def split_data(**kwargs):
    """
    Realiza un split del archivo `data_1.csv` en conjuntos de entrenamiento y prueba, y los guarda en la carpeta `splits`.
    """
    execution_date_str = kwargs.get("execution_date", datetime.now().strftime('%Y-%m-%d'))
    execution_date = datetime.strptime(execution_date_str, "%Y-%m-%d")
    base_folder = f"dags/{execution_date.strftime('%Y-%m-%d')}"
    raw_path = os.path.join(base_folder, "raw", "data_1.csv")
    splits_path = os.path.join(base_folder, "splits")

    # Leer el archivo CSV
    data = pd.read_csv(raw_path)

    # Separar variables predictoras y objetivo
    X = data.drop(columns=["HiringDecision"])
    y = data["HiringDecision"]

    # Dividir los datos manteniendo la proporción
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=333
    )

    # Guardar los conjuntos de datos
    os.makedirs(splits_path, exist_ok=True)
    X_train.to_csv(os.path.join(splits_path, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(splits_path, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(splits_path, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(splits_path, "y_test.csv"), index=False)

    print(f"Datos divididos y guardados en: {splits_path}")


# 3. preprocess_and_train()
def preprocess_and_train(**kwargs):
    """
    Preprocesa los datos y entrena un modelo RandomForest. Guarda el modelo entrenado en la carpeta `models`.
    """
    # Obtener la fecha de ejecución
    execution_date_str = kwargs.get("execution_date", datetime.now().strftime('%Y-%m-%d'))
    execution_date = datetime.strptime(execution_date_str, "%Y-%m-%d")
    base_folder = f"dags/{execution_date.strftime('%Y-%m-%d')}"
    splits_path = os.path.join(base_folder, "splits")
    models_path = os.path.join(base_folder, "models")

    # Leer los conjuntos de datos
    X_train = pd.read_csv(os.path.join(splits_path, "X_train.csv"))
    X_test = pd.read_csv(os.path.join(splits_path, "X_test.csv"))
    y_train = pd.read_csv(os.path.join(splits_path, "y_train.csv")).squeeze()
    y_test = pd.read_csv(os.path.join(splits_path, "y_test.csv")).squeeze()

    # Identificar características numéricas y categóricas
    numeric_features = [
        "Age",
        "ExperienceYears",
        "PreviousCompanies",
        "DistanceFromCompany",
        "InterviewScore",
        "SkillScore",
        "PersonalityScore",
    ]
    categorical_features = ["Gender", "EducationLevel", "RecruitmentStrategy"]

    # Crear el preprocesador
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    # Crear el pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(random_state=333)),
        ]
    )

    # Entrenar el modelo
    pipeline.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, pos_label=1)

    print(f"Accuracy en el conjunto de prueba: {accuracy:.2f}")
    print(f"F1-Score (clase positiva): {f1:.2f}")

    # Guardar el modelo entrenado
    os.makedirs(models_path, exist_ok=True)
    model_path = os.path.join(models_path, "model.joblib")
    joblib.dump(pipeline, model_path)
    print(f"Modelo guardado en: {model_path}")


# 4. Gradio
def predict(file, model_path):

    pipeline = joblib.load(model_path)
    input_data = pd.read_json(file)
    predictions = pipeline.predict(input_data)
    labels = ["No contratado" if pred == 0 else "Contratado" for pred in predictions]
    
    return {"Predicción": labels[0]}


def gradio_interface(**kwargs):
    execution_date_str = kwargs.get("execution_date", datetime.now().strftime('%Y-%m-%d'))
    execution_date = datetime.strptime(execution_date_str, "%Y-%m-%d")
    model_path = f"dags/{execution_date.strftime('%Y-%m-%d')}/models/model.joblib"

    interface = gr.Interface(
        fn=lambda file: predict(file, model_path),
        inputs=gr.File(label="Sube un archivo JSON"),
        outputs="json",
        title="Hiring Decision Prediction",
        description="Sube un archivo JSON con las características de entrada para predecir si Nico será contratado o no.",
    )
    interface.launch(share=True)