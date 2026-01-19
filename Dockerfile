FROM python:3.9-slim

WORKDIR /app

COPY . .

# Mise à jour pip et installation des 3 librairies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Lancement sans sécurité bloquante
CMD ["streamlit", "run", "app.py", \
    "--server.port=8080", \
    "--server.address=0.0.0.0", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=false", \
    "--server.fileWatcherType=none", \
    "--browser.gatherUsageStats=false"]
