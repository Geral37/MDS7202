from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.utils.dates import days_ago

from hiring_functions import create_folders, split_data, preprocess_and_train, gradio_interface
import os
import subprocess
from datetime import datetime
import gradio as gr

args = {
    'owner': 'MDS7202',
    'retries': 1,
}

dag_id = "hiring_pipeline"
fecha_inicio = datetime(2024, 10, 1)

with DAG(
    dag_id=dag_id,
    default_args=args,
    description='Pipeline intento 28374913',
    start_date=days_ago(5),
    schedule_interval=None,
    catchup=False  # Sin backfill: entrenamiento retroactivo para cubrir tareas no ejecutadas que debieron haberlo sido o algo así entendí
) as dag:
    
    # Task 1 - Start
    start_pipeline = EmptyOperator(task_id='Start')

    # Task 2 - Create folders
    create_folders_task = PythonOperator(
        task_id="create_folders",
        python_callable=create_folders,
        op_kwargs={"execution_date": "{{ ds }}"},
    )

    # Task 3 - Download data
    download_dataset_task = BashOperator(
        task_id='download_dataset',
        bash_command=(
            "curl -o dags/{{ ds }}/raw/data_1.csv "
            "https://gitlab.com/eduardomoyab/laboratorio-13/-/raw/main/files/data_1.csv"
        )
    )

    # Task 4 - Split data
    split_data_task = PythonOperator(
        task_id="split_data",
        python_callable=split_data,
        op_kwargs={"execution_date": "{{ ds }}"},
    )

    # Task 5 - Preprocess and train the model
    preprocess_and_train_task = PythonOperator(
        task_id="preprocess_and_train",
        python_callable=preprocess_and_train,
        op_kwargs={"execution_date": "{{ ds }}"},
    )

    # Task 6 - Run Gradio interface
    gradio_interface_task = PythonOperator(
        task_id="gradio_interface",
        python_callable=gradio_interface,
        op_kwargs={"execution_date": "{{ ds }}"},
    )

    # Task 7 - End
    end_pipeline = EmptyOperator(task_id='End')

    # Define the workflow process
    start_pipeline >> create_folders_task
    create_folders_task >> download_dataset_task
    download_dataset_task >> split_data_task
    split_data_task >> preprocess_and_train_task
    preprocess_and_train_task >> gradio_interface_task
    gradio_interface_task >> end_pipeline