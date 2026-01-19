FROM python:3.9-slim

# On installe le strict minimum pour que ça aille plus vite
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# LA LIGNE MAGIQUE : On désactive toutes les sécurités bloquantes via des "flags"
CMD ["streamlit", "run", "app.py", \
    "--server.port=8080", \
    "--server.address=0.0.0.0", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=false", \
    "--server.fileWatcherType=none", \
    "--browser.gatherUsageStats=false"]
