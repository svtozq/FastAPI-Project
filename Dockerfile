FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Vérifie que l'application se charge sans erreur
CMD ["python", "-c", "import main"]
