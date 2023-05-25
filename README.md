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
git clone https://github.com/GCTMLP/otus_hasker.git
```
2. Go to folder
```
cd otus-hasker
```
3. Run docker containers in developer mode (if you want to add and test some changes)
```
docker-compose -f docker-compose.yml up -d --build
```
4. Or run docker containers in production mode
```
docker-compose -f docker-compose.prod.yml up -d --build
```
