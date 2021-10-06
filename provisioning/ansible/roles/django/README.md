### README
- Pokud je "default_robots=True" tak se vytvoří /var/www/project_name/static/robots.txt, který je servírován přímo nginxem
- Pokud je "default_robots=False" tak nevytvoří soubor automaticky a je nutné jej řešit aplikačně přes collectstatic, tak aby byl na stejném místě 

