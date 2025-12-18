# Image de base : Python officiel
FROM python:3.11-slim

# Définir le dossier de travail dans le container
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code backend dans le container
COPY . .

# Exposer le port utilisé par FastAPI
EXPOSE 8000

# Lancer FastAPI avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
