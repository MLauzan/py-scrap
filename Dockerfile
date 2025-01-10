# Usar una imagen base de Python
FROM python:3.9-slim

# Instalar dependencias del sistema para Selenium y Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    libx11-dev \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libappindicator3-1 \
    libnspr4 \
    libnss3 \
    libxtst6 \
    libxrandr2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgdk-pixbuf2.0-0 \
    && apt-get clean

# Instalar Google Chrome
RUN wget -q -O - https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > google-chrome.deb \
    && dpkg -i google-chrome.deb \
    && apt-get -f install -y \
    && rm google-chrome.deb

# Instalar dependencias de Python
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . /app

# Configuración del puerto en el que se ejecuta la aplicación Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
