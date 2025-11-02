py -3 -m venv .venv
.venv\Scripts\activate
pip install --no-cache-dir -r requirements.txt

python -m waitress --port=3723 main:app 

docker-compose up --build


# Début sur dev
git checkout dev

# Travail et commits
git add .
git commit -m "Nouvelle fonctionnalité"
git push origin dev

# Fusion dans main via merge
git checkout main
git pull origin main
git merge dev
git push origin main

# Retour sur dev
git checkout dev


