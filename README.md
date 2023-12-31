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

## Переменная окружения.
**В корневой папке создать файл расширения _.env_**
```
SECRET_KEY=XXXXXX
DEBUG=XXXX
ALLOWED_HOSTS=XXXXXX XXXXXXX # Перечислить все необходимые хосты через пробел.
```
Для базы данных Postgresql указать следуюшие переменные:
```
NAME=XXXXXXXX
DB_USER=XXXXXXXX
PASSWORD=XXXXXXXX
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

### Выполните инструкции для создания и наполнения базы данных и создания суперпользователя:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
### Для полноценной работы неоходимо:

***Проверить работает ли сервер Redis.***

```
redis-cli ping # Овет PONG
```
***Запустить рабочего Celery.***

```
celery -A make_yourself worker -l INFO
```

**Запустите сервер Django:**

```
python manage.py runserver
```

**По умолчанию проект работает на порту 8000.**


Для просмотра swagger документации используйется

http://localhost:8000/api/schema/docs/

## Диаграмма связей бизнес-сущностей

![model_diagram.svg](model_diagram.svg)
