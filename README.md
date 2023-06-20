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
SOCIAL_AUTH_VK_OAUTH2_KEY="*****"       # ID приложения VK
SOCIAL_AUTH_VK_OAUTH2_SECRET="*****"    # Защищённый ключ VK
```
Переменная окружения `DATABASE_URL` собирается из следующих значений:
* user: как в `POSTGRES_USER`
* password: как в `POSTGRES_PASSWORD`
* host: по умолчанию `localhost`
* port: по умолчанию `5432`
* database: как в `POSTGRES_DB`

Все переменные начинающиеся на `POSTGRES` нужны для корректной работы самой базы данных. Данный переменные указаны в [docker-compose.yaml](./infra/docker-compose.yaml).

Запуск через Docker Compose:
```shell
docker-compose --env-file .env -f infra/docker-compose.yaml up -d
```
___
### Аутентификация и авторизация.
С помощью frontend-приложения можно выполнить следующие функции:
- [x] регистрация,
- [x] вход/выход,
- [x] получение и обновление профиля,
- [x] смена пароля,
- [x] вход через социальную сеть VK.

Методы валидации паролей описаны в [сериализаторах](./todolist/core/serializers.py). 
Минимальная длина пароля установлена в 10 символов. 
___
### Telegaram bot
Бот доступен по [ссылке](https://t.me/dlbzh_todolist_bot)
С его помощью можно создавать цели и выводить список текущих целей. 
Шаблоны сообщений выполнены при помощи Jinja2.
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
7. ~~Выгрузка целей в CSV/JSON.~~
8. ~~Заметки к целям.~~
9. ~~Все перечисленный функции должны быть реализованы в мобильном приложении.~~

___
#### <p align="center">list of problems</p>
1. localization 
`OSError: No translation files found for default language "ru-RU".`
https://www.django-rest-framework.org/topics/internationalization/
https://docs.djangoproject.com/en/4.0/topics/i18n/translation/#how-django-discovers-language-preference