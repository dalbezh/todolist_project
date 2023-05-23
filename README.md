# <p align="center">TODOLIST</p>

### Приложение для планирования целей

---
### Technology stack:
[![Python](https://img.shields.io/badge/python-v3.9-orange)](https://www.python.org/downloads/release/python-394/)
[![Django](https://img.shields.io/badge/django-v4.0.1-green)](https://docs.djangoproject.com/en/4.2/releases/4.0.1/)
[![Postgres](https://img.shields.io/badge/postgres-v12.4-blue)](https://www.postgresql.org/docs/12/release-12-4.html)
___
### Как локально запустить приложение:

Сначала необходимо установить зависимости:
```shell
pip install -r requirements.txt
```
В корне проекта нужно создать файл `.env`, и заполнить в нём следующие значения:
```
DEBUG=True                              # по умолчанию для локального окружения - True
SECRET_KEY="*****"                      # значение из settings.py
POSTGRES_USER=...                       # имя пользователь БД
POSTGRES_PASSWORD=...                   # пароль пользователя БД
POSTGRES_DB=...                         # название БД 
DATABASE_URL=psql://user:password@host:port/database
```
Переменная окружения `DATABASE_URL` собирается из следующих значений:
* user: как в `POSTGRES_USER`
* password: как в `POSTGRES_PASSWORD`
* host: по умолчанию `localhost`
* port: по умолчанию `5432`
* database: как в `POSTGRES_DB`

Все переменные начинающиеся на `POSTGRES` нужны для корректной работы самой базы данных. Данный переменные указаны в [docker-compose.yaml](./infra/docker-compose.yaml).

Запуск БД через Docker Compose:
```shell
docker-compose --env-file ./.env -f ./infra/docker-compose.yaml up -d
```
Создание и применение миграций:
```shell
cd todolist/
./manage.py makemigrations
./manage.py migrate
```
Запуск приложения:
```shell
./manage.py runserver
```
___
### Application functionality:
1. Вход/регистрация/аутентификация через вк.
2. Создание целей.
   * Выбор временного интервала цели с отображением кол-ва дней до завершения цели.
   * Выбор категории цели (личные, работа, развитие, спорт и т. п.) с возможностью добавлять/удалять/обновлять категории.
   * Выбор приоритета цели (статичный список minor, major, critical и т. п.).
   * Выбор статуса выполнения цели (в работе, выполнен, просрочен, в архиве).
3. Изменение целей.
   * Изменение описания цели.
   * Изменение статуса.
   * Дать возможность менять приоритет и категорию у цели.
4. Удаление цели.
   * При удалении цель меняет статус на «в архиве».
5. Поиск по названию цели.
6. Фильтрация по статусу, категории, приоритету, году.
7. Выгрузка целей в CSV/JSON.
8. Заметки к целям.
9. Все перечисленный функции должны быть реализованы в мобильном приложении.