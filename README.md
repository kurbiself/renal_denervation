# Серверная часть веб-приложения "Регистр ренальной денервации"

## Содержание

- [Описание проекта](#title1)
- [Технологии](#title2)
- [Установка и запуск](#title3)
- [Разработка](#title1_4)

## <a id="title1">Описание проекта</a>

Веб-приложения предназначено для ведения регистра данных клинической практики применения нового интервенционного лечения артериальной гипертонии — _ренальной денервации_. Решение актуально в условиях отсутствия централизованного учета данных по данному методу лечения резистентной артериальной гипертензии (АГ) в России

## <a id="title2">Описание проекта</a>

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)

Основной стек:

- Backend: Python + Django REST Framework
- Database: PostgreSQL
- Аутентификация: JWT + Custom User Model

## <a id="title1_3">Установка и запуск</a>

### 1. Клонирование репозитория

```bash
git clone https://github.com/kurbiself/renal_denervation.git
cd renal-denervation
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Запуск сервера

```bash
python manage.py migrate
python manage.py runserverf
```

### 4. Настройка БД

1. Установите PostgreSQL 16
2. Создайте базу данных:

```bash
CREATE DATABASE renal_denervation;
CREATE USER rd_user WITH PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE renal_denervation TO rd_user;
```

3. Настройте подключение в settings.py:

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```
