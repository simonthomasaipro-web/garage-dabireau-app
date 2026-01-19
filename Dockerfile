FROM python:3.9-slim

# 1. Installation des outils système (Linux)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# 2. Mise à jour de l'installateur Python
RUN pip install --upgrade pip

# 3. Installation des librairies de ton app
RUN pip install --no-cache-dir -r requirements.txt

# 4. LE SECRET EST ICI : Création du fichier de config Streamlit
# On force la désactivation des sécurités qui bloquent l'upload sur Cloud Run
RUN mkdir -p ~/.streamlit
RUN echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
enableWebsocketCompression = false\n\
" > ~/.streamlit/config.toml

EXPOSE 8080

# 5. Lancement de l'application
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
