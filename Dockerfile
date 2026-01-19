FROM python:3.9-slim

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# ASTUCE : Cette ligne force Google a voir que le fichier a changé
RUN pip install --upgrade pip

# On installe les librairies (cette fois il va bien lire le nouveau requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
