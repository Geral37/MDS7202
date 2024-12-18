# Utiliza una imagen base con Python instalado
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /root/airflow

# Establece la variable de entorno AIRFLOW_HOME
ENV AIRFLOW_HOME=/root/airflow

# 
# Elimina ejemplos
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libgomp1 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala Apache Airflow
RUN pip install apache-airflow
RUN pip install pandas
RUN pip install numpy
RUN pip install xgboost
RUN pip install joblib
RUN pip install scikit-learn==1.5.2

# Inicializa la base de datos de Airflow
RUN airflow db init

# Expone el puerto 8080 para el servidor web de Airflow
EXPOSE 8080

# Crea el usuario admin de Airflow
RUN airflow users create --role Admin --username admin --email admin \
 --firstname admin --lastname admin --password admin

# Copia las carpetas necesarias al contenedor
COPY ./dags $AIRFLOW_HOME/dags
COPY ./models $AIRFLOW_HOME/models
COPY ./data $AIRFLOW_HOME/data
COPY ./logs $AIRFLOW_HOME/logs

# Comando para iniciar el servidor web y el scheduler
CMD ["sh", "-c", "airflow webserver -p 8080 & airflow scheduler"]
