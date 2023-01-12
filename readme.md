## Neftekamsk Reality Bot

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![aiogram](https://img.shields.io/badge/aiogram-asyncio%20telegram-brightgreen)](https://aiogram.dev/)

Pet-проект телеграм бота и базы данных объектов для риелторов города. В принципе, привязки к городу как таковой нет, бот можно использовать где угодно.
Присутствие в названии бота топонима Ntftekamsk направлено лишь на его узнаваемость среди риелторского сообщества города.
Отсутствие единой базы объектов приводит к тому, что риелторы города с трудом срабатываются друг с другом за пределом своего агентства.
Для того, чтобы сработаться с другим риелтором, агент проводит много времени в поиске объектов, "копаясь" в авито, вконтакте и др. площадках.
Даже существующий чат риелторов города не даёт нужного эффекта из-за засоренности нетематическими сообщениями (флудом).

Данный проект решает эту проблему.
С помощью бота можно работать как с объектами, так и с покупателями:

- завести новый объект в общую базу
- удалить свой объект из базы
- редактировать цену своего объекта при необходимости
- просмотреть все свои объекты
- просмотреть объекты других риелторов
- завести покупателя в свою базу (видимость только для риелтора)
- удалить покупателя при необходимости
- просмотреть всех своих покупателей
- просмотреть подходящие объекты из общей базы для своего клиента
- во время добавления агентом нового покупателя, при наличии подходящих объектов, риелторам этих объектов отправляется сообщение, что у такого-то агента появился
подходящий клиент для твоего объекта.

Бот написан на языке Python, с использованием библиотеки aiogram, инструментов Django ORM. База данных работает на основе PostgreSQL. Проект запущен в
контейнерах с помощью Docker.

### Запуск проекта
- склонировать на локальную машину
- создать рядом с manage.py (в папке bot) файл *.env параметров виртуального окружения
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DJ_SECRET_KEY='django_secret_key'

TELEGRAM_TOKEN=токен_вашего_бота
```
- запустить контейнеры docker. Автоматом установятся зависимости и запустится сервер django
```
docker-compose up -d --build
```
- в контейнере backend с ботом проделать миграции и создать суперпользователя
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
- запустить бот командой
```
python manage.py aio_bot
```

Готово!
