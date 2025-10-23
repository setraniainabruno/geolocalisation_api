py -3 -m venv .venv
.venv\Scripts\activate
pip install --no-cache-dir -r requirements.txt

python -m waitress --port=3723 main:app 

docker-compose up --build


