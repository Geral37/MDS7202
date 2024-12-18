from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# IMPORTANTE: Los estudiantes deben implementar las funciones necesarias en un archivo aparte.
from functions_exam import clean_data, check_and_join_data, inference, preprocess

args = {
    'owner': 'MDS7202',
    'retries': 1,
}

with DAG(
    dag_id='Accidentes',
    default_args=args,
    description='MLops pipeline',
    start_date=days_ago(3), # COMPLETAR: Reemplazar con la información entregada en el enunciado
    schedule_interval='@daily', # COMPLETAR: Reemplazar con la información entregada en el enunciado
    catchup=True # COMPLETAR: Reemplazar con la información entregada en el enunciado
) as dag:
    
    # Task 1 - Inicio del DAG
    dummy_task = EmptyOperator(task_id='Start', retries=2)

    # Task 2 - Descargar el dataset limpio
    # Los estudiantes deben completar la configuración de esta tarea usando BashOperator
    task_download_dataset_limpio = BashOperator(
        task_id='download_dataset_limpio',
        bash_command="curl -o "
        "/Proyecto/Airflow/data/data_limpia.csv "
        "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/exam/data_limpia.csv"
    )
    # Task 3 - Descargar el dataset sucio
    # Los estudiantes deben completar esta tarea de manera similar a la anterior
    task_download_dataset_sucio = BashOperator(
        task_id='download_dataset_sucio',
        bash_command="curl -o "
        "/Proyecto/Airflow/data/data_sucia.csv "
        "https://gitlab.com/imezadelajara/datos_clase_7_mds7202/-/raw/main/exam/data_sucio.csv"
    )

    # Task 4 - Limpiar los datos
    # Los estudiantes deben implementar la función `clean_data` en un archivo externo
    task_clean_data = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data,  # COMPLETAR: Reemplazar con la función clean_data
        op_kwargs= {'data_name': 'data_sucia.csv'} # COMPLETAR: Reemplazar con el argumento esperado
    )

    # Task 5 - Verificar y combinar los datos
    # Los estudiantes deben implementar la función `check_and_join_data` en un archivo externo
    task_check_and_join_data = PythonOperator(
        task_id='check_and_join_data',
        python_callable=check_and_join_data,  # COMPLETAR: Reemplazar con la función check_and_join_data
        trigger_rule='all_success' # COMPLETAR: Reemplazar con el trigger solicitado
    )

    # Task 6 - Generar predicciones
    # Los estudiantes deben implementar la función `inference` en un archivo externo
    task_inference = PythonOperator(
    task_id='inference',
    python_callable=inference
    )

    # Task 7 - Finalizar el DAG
    final_dummy_task = EmptyOperator(task_id='End', retries=1)

    # Definir el flujo de trabajo
    dummy_task >> [task_download_dataset_limpio, task_download_dataset_sucio]
    # Complete con su codigo... 
    task_download_dataset_sucio >> task_clean_data
    task_download_dataset_limpio >> check_and_join_data
    task_clean_data >> check_and_join_data
    check_and_join_data >> task_inference
    task_inference >> final_dummy_task
   