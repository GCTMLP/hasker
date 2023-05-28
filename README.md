# Hasker
poor man`s stackoverflow

# Online version
https://gctmlp.ru/

# About

This is educational project to show my skills, which functional is similar to stackoverflow.com

Technology stack is:
  - Nginx
  - gunicorn
  - Django
  - Vue.js
  - Postgresql
  - Docker/docker-compose
  - Smarty templates

# How to deploy

1. Clone the repository
```
git clone https://github.com/GCTMLP/hasker.git
```
2. Clone the repository with staticfiles (CSS, JS)
```
git clone https://github.com/GCTMLP/assets.git
```
3. Copy assets to hasker project
```
cp -R asssets hasker/static
```
4. Go to folder
```
cd otus-hasker
```
5. Create files .env.dev (if you want to add and test some changes) or .env.prod with your sensitive data.

File structure like:
```
DEBUG=0
SECRET_KEY=SECRET_KEY
ALLOWED_HOSTS=www.your_host.ru
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=db_name
SQL_USER=db_user
SQL_PASSWORD=db_password
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
EMAIL_HOST=smtp.gmail.com
EMAIL_ADDRESS=your_mail
EMAIL_PASSWORD=mail_password
```

6. Run docker containers in developer mode (if you want to add and test some changes)
```
docker-compose -f docker-compose.yml up -d --build
```
7. Or run docker containers in production mode
```
docker-compose -f docker-compose.prod.yml up -d --build
```
