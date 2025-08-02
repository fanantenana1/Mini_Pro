FROM python:3.11

# Création d’un utilisateur non root
RUN useradd -m flask

# Répertoire de travail
WORKDIR /home/flask

# Copie du code source
COPY . .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Attribution des droits
RUN chmod a+x app.py test.py && chown -R flask:flask ./

# Variables d’environnement
ENV FLASK_APP=app.py

# Port d’écoute
EXPOSE 5000

# Utilisateur non root
USER flask

# Commande de lancement
CMD ["python", "app.py"]
