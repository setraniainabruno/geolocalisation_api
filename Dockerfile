# Étape 1 : Image de base
FROM python:3.11-alpine

# Étape 2 : Répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers
COPY requirements.txt .

# Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier le code source
COPY . .

# Étape 6 : Exposer le port Flask
EXPOSE 3723

# Étape 7 : Commande de lancement
CMD ["python", "-m", "waitress", "--listen=*:3723", "main:app"]
