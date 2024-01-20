# Table of Contents
1. [Функционал приложения](#функционал-приложения)
2. [Используемый стек технологий](#используемый-стек-технологий)
3. [Инструкция для запуска](#инструкция-для-запуска) 
   1. [Переменные окружения](#переменные-окружения)
   2. [Инструкции БД и суперпользователя](#выполните-инструкции-для-создания-и-наполнения-базы-данных-и-создания-суперпользователя)
   3. [Проверка Redis](#проверить-работает-ли-сервер-redis)
   3. [Запуск Celery](#запустить-рабочего-celery)
   3. [Запуск Djsngo-server](#запустите-сервер-django)
4. [Swagger документация](#swagger)
5. [Диаграмма БС](#диаграмма-связей-бизнес-сущностей)
6. [Инструкция Docker](#docker---инструкция-по-запуску)
   1. [settings.py](#settingspy)
   2. [Переменные окружения docker](#envdocker)
   3. [Запуск docker](#запуск-docker)







# Функционал приложения.

Приложение создано для упрощения запоминания материала посредством тестов.
Включает возможность проходить тесты по различным
тематикам(будут добавлены позже), создавать и редактировать свои собственные
тесты для повторения и заучивания тем.
Есть возможность создавать и редактировать посты к блогу.
Возможность создавать и редактировать конспекты и связывать их с
тестами(будут добавлены позже).

# Используемый стек технологий.
- Python
- Django
- Django Rest Framework
- Celery
- Redis
- Swagger

# Инструкция для запуска.

## Переменные окружения.
**В корневой папке создать файл расширения _.env_**
```
SECRET_KEY=XXXXXX
DEBUG=XXXX
ALLOWED_HOSTS=XXXXXX XXXXXXX # Перечислить все необходимые хосты через пробел.
```
Для базы данных Postgresql указать следуюшие переменные:
```
POSTGRES_DB=XXXXXXXX
POSTGRES_USER=XXXXXXXX
POSTGRES_PASSWORD=XXXXXXXX
HOST=XXXXXXXX
```
Для работы почты укажите в переменных настройки приложения для вашей почты
```
EMAIL_USE_TLS=XXXXXXXX
EMAIL_USE_SSL=XXXXXXXX
EMAIL_HOST=XXXXXXXX
EMAIL_HOST_USER=XXXXXXXX
EMAIL_HOST_PASSWORD=XXXXXXXX
EMAIL_PORT=XXXXXXXX
DEFAULT_FROM_EMAIL=XXXXXXXX
```

## Выполните инструкции для создания и наполнения базы данных и создания суперпользователя:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Проверить работает ли сервер Redis.

```
redis-cli ping # Овет PONG
```
## Запустить рабочего Celery.

```
celery -A make_yourself worker -l INFO
```

## Запустите сервер Django:

```
python manage.py runserver
```

**По умолчанию проект работает на порту 8000.**

# Swagger
Для просмотра swagger документации используйется

http://localhost:8000/api/schema/docs/

# Диаграмма связей бизнес-сущностей

![model_diagram.svg](model_diagram.svg)

# Docker - инструкция по запуску

### settings.py

Поменять настройки в settings.py, одни закомментировать, другие раскомментировать:
```
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
```
### .env.docker
Создать файл .env.docker с теми же настройками как и указанный выше [.env](#переменные-окружения),
и добавить в него переменные, со значениями доступа к базе данных:
```
DB_HOST=XXXXXX
DB_NAME=XXXXXX
DB_USER=XXXXXX
DB_PASS=XXXXXX
```

### Запуск Docker
Запустить из корневой папки в терминале:
```
docker compose up
```
Сайт будет доступен на порту:
http://0.0.0.0:8001