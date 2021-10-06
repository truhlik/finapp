# Instalace nového serveru
kapitálkama jsou v readme proměnné, které je třeba doplnit

## Requirements
- python
- pip
- backup disk mounted to /mnt/backup s právy pro zápis uživatele adminstator

## Deploy
```
ansible-playbook deploy_develop.yml -u administrator
```

## Start new server (všechno děláš na localu)
- Nainstalovat ansible     
```
pip install -r requirements.txt
```

- Nainstalovat role  
```
ansible-galaxy install -r requirements.yml
```

- Přidej do hosts záznam  
POZOR před hostname nesmí být uživatelské jméno jinak nefunguje auth bez klíče   
```
[SERVER_GROUP_NAME]
SERVER_HOSTNAME
```
- vytvoř si vault.txt s heslem k odemčení vault.yml

- pokud potřebuješ, tak si přenastav proměnné v odpovídajících vars.yml souboru

- Nainstaluj server a nakonfiguruj vše potřebné  
(pokud to selže napoprvé na postgres, tak viz. TODO)  
```
ansible-playbook setup_production.yml -u USER --become-method su --become-user root --ask-become --ask-pass
```
První heslo je pro uživatele USER.  
Druhé heslo je pro uživatele root.  

- Každé další nasazení je už pouze takto  
```
ansible-playbook setup_production.yml -u USER
```

## Start new Django project
- Nastav DNS pro získání certifikátu
- Nastav proměnné pro tento projekt v `group_vars/ENV/vars.yml`
- Nastav v `hosts` adresu serveru
- Nainstalovat ansible 
```
pip install -r requirements.txt
```

- Nainstalovat role  
```
ansible-galaxy install -r requirements.yml
```

- Vytvořit klíč k decryptování vault (LastPass)  
```
echo VAULT_PASSWORD > vault.txt
```
- Vlož do vaultu heslo k DB (vygeneruj)
```
ansible-vault edit group_vars/all/vars_vault.yml
```
- Nainstaluj projekt   
```
ansible-playbook deploy_production.yml -u administrator
```

## MIGRATE DB AND MEDIA
```
ansible-playbook migrate_project.yml --extra-vars "host1=hosting2.endevel.cz host2=hosting3.endevel.cz -u administrator"
```

## TODO
- backup (almost done)
- monitoring (https://github.com/felipesantiago/ansible-uptimerobot)
- postgres vytvoření uživatele napoprvé nejde, stačí zakomentovat pro první nasazení a při druhém to již projde
