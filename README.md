# Instalace na lokalním prostředí

## Requirements
postgis

### Packages
python-3.7.3  

## Start project

Docker

```bash
docker-compose up --build
```

Lokálně
Doporučuju pouze docker-compose - je tam volume, takže když to zapnete, můžete
normálně editovat a web se vám reoaduje v dockeru stejně jako by byl na lokálu.

Debug přes testy.

....ale pokud po tom někdo touží, tak budiž:

```
git clone git@gitlab.com:endevel/internal/projects/tisknu.git
cd tisknu
mkvirtualenv -p /usr/bin/python3.7.3 tisknu
pip install -r requirements/local.pip
cp .env.sample .env
```    

~~cp main/settings/local.py.sample main/settings/local.py~~

III. Nastav si lokální settingy v souboru `main/settings/local.py` - volitelné.  
IV. Nastav si proměné prostředí  
 - DJANGO_SETTINGS_MODULE = main.setttings.localhost
 - GOOGLE_APPLICATION_CREDENTIALS = service-account-gcs.json

V. Vytvoř si databázi v Postgresql, napr.:
Stejně jako předtím - docker-compose

```
sudo -u postgres psql
CREATE USER tisknu WITH PASSWORD 'tisknu';
CREATE DATABASE tisknu OWNER tisknu;
GRANT CONNECT ON DATABASE tisknu TO tisknu;
\c tisknu;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO tisknu;

```
VI. Uprav si proměnné v souboru `.env` 
    - určitě bude potřeba nastavit DB připojení k tvé lokální postgres db
    - pokud nepoužíváš smtp backend, tak nemusíš vyplňovat věci pro nastavení mailingu
    
VII. Vytvoř si tabulky v DB `./manage.py migrate`

VII. Spusť projekt `./manage.py runserver`


---------------
# kubernetes
```bash
kubectl port-forward svc/cloudsqlproxy 9999:5432
psql postgres://tisknu@localhost:9999/tisknu
kubectl get secret tisknu-back -ojsonpath={.data.db_password} | base64 --decode

drop schema public cascade;
 create schema public;

```