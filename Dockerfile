FROM python:3.9-slim

# Ajout de libgomp1 (CRUCIAL pour que l'IA ne plante pas)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# On force la mise à jour de pip
RUN pip install --upgrade pip

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# On lance Streamlit en désactivant certaines sécurités qui bloquent l'affichage sur Cloud Run
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.address", "0.0.0.0", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
