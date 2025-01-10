FROM selenium/standalone-chrome

# Instalar tus dependencias de Python
RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copiar tu aplicación
COPY . /app
WORKDIR /app

CMD ["python3", "script.py"]
