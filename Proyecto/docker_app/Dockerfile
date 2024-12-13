# Usa una imagen ligera de Python como base
FROM python:3.10-slim

# Instala las herramientas necesarias para ambos servicios
RUN apt-get update && apt-get install -y curl

# Establece el directorio de trabajo
WORKDIR /app

# Copia las dependencias
COPY /app/requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Comando por defecto (puedes sobrescribirlo en docker-compose)
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
