FROM python:3.9-slim

# Installation des outils pour l'image
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
