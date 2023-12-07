# Foodgram
    chizhovsky-foodgram.ddns.net

### Описание:
Foodgram - это сервис для публикации рецептов. Пользователю доступны главная страница, страница рецептов, возможность 
добавления нового рецепта и его редактирование. Возможность подписаться на любимого автора и отписаться от надоевшего. 
Можно добавить любимый рецепт (например, вареное яичко) в избранное. Есть возможность добавлять рецепты в корзину. 
А затем этот список для покупок скачать.

Почта для входа в панель администратора: admin@gmail.com  
Пароль: Aa0000

## Технологии
- Python 3.9
- Django 3.2
- Django REST framework 3.14
- Gunicorn 21.2.0
- Djoser 2.2.0
- Docker
- PostgreSQL

## Установка
1. Склонируйте репозиторий.
```
git clone git@github.com:chizhovsky/foodgram-project-react.git
```
<br>

2. Скомпилируйте проект, используя docker.
```
docker compose up -d
```
<br>

3. Выполните миграции, соберите статику.
```
docker compose exec infra-backend-1 python3 manage.py migrate
docker compose exec infra-backend-1 python3 manage.py collectstatic
docker compose exec infra-backend-1 cp -r app/static/. ../static/
```
<br>

## Примеры API
Регистрация пользователя
```
POST http://localhost/api/users/

{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```

Создание рецепта
```
POST http://localhost/api/recipes/

{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

## Пример .env
```
POSTGRES_USER=fdjango_user
POSTGRES_PASSWORD="пароль от базы данных"
POSTGRES_DB=postgres_db
DB_HOST=db
DB_PORT=5432
SECRET_KEY="секретный ключ"
DEBUG=False
ALLOWED_HOSTS="хосты через запятую"
```

## Автор
[Алексей Чижов](https://github.com/chizhovsky)