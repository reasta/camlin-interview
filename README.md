activate venv:
.\.venv\Scripts\activate

install requirements:
pip install -r requirements.txt       


run server:
#fastapi dev main.py
cd app
uvicorn main:app --reload

linting"python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.lintOnSave": true








DECKER
docker exec -it python-container /bin/bash  -> pokretanje kontejenra sa nazivom "python-container"
docker exec -it mysql-container bash
mysql -u camlin -p
SHOW DATABASES;

docker-compose down --volumes --remove-orphans  -> sklanjanje cachea
docker system prune --all --force  -> brisanje prethodnih kontejera i slika

docker-compose up --build  -> pokretanje
docker-compose down  -> gasenje