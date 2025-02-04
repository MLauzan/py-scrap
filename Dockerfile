FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos del proyecto
COPY . .

# Establecer la variable de FLASK_APP
ENV FLASK_APP=script.py

# Establecer el puerto
ENV PORT=5000

# Exponer el puerto
EXPOSE $PORT

# Usar shell para correr el programa
CMD flask run --host=0.0.0.0 --port=$PORT
