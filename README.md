# Foodgram
    chizhovsky-foodgram.ddns.net

### Описание:
Foodgram - это сервис для публикации рецептов. Пользователю доступны главная страница, страница рецептов, возможность 
добавления нового рецепта и его редактирование. Возможность подписаться на любимого автора и отписаться от надоевшего. 
Можно добавить любимый рецепт (например, вареное яичко) в избранное. Есть возможность добавлять рецепты в корзину. 
А затем этот список для покупок скачать.

Почта для входа в панель администратора: admin@mail.com  
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
Склонируйте репозиторий.
```
git clone git@github.com:chizhovsky/foodgram-project-react.git
```
<br>

Скомпилируйте проект, используя docker.
```
docker compose up -d
```
<br>

Выполните миграции, соберите статику.
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
  "email": "peter-parker@mail.com",
  "username": "peter-parker",
  "first_name": "Peter",
  "last_name": "Parker",
  "password": "spider-man123"
}
```

Создание рецепта
```
POST http://localhost/api/recipes/

{
  "ingredients": [
    {
      "id": 233,
      "amount": 8
    }
  ],
  "tags": [
    breakfast,
    lunch
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAHhbjinfjjbiAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKdgggdUbkHoAAAAggCByxOyYQAAAABJRU5ErkJggg",
  "name": "Вареное яйцо",
  "text": "Сварите в воде! ",
  "cooking_time": 7
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
