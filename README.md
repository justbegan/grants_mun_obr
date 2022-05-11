for dev
```
cp env.example .env
docker-compose build
docker-compose up
docker-compose exec web python manage.py createsuperuser
```
dump db

```
docker-compose exec db pg_dump -U postgres $POSTGRES_DB > back.sql
```

restore db

```
docker cp back.sql "$(docker-compose ps -q db)":/
docker-compose exec db dropdb -U postgres postgres
docker-compose exec db createdb -U postgres postgres
docker-compose exec db psql -U postgres -d postgres -f /back.sql
```




for prod
```
cp env.example .env
docker-compose -f docker-compose.prod.yaml build
docker-compose -f docker-compose.prod.yaml up
docker-compose -f docker-compose.prod.yaml exec web python manage.py createsuperuser

```

На сервере, команда перезапуска как демон
```
 docker-compose -f docker-compose.prod.yaml up -d --build
```
