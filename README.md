# Используемый стек технологий.
- Python
- Django
- Django Rest Framework
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

**Запустите сервер Django:**

```
python manage.py runserver
```

**По умолчанию проект работает на порту 8000.**


Для просмотра swagger документации используйется

http://localhost:8000/api/schema/docs/
