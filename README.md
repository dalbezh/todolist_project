# <p align="center">TODOLIST</p>
### <p align="center">Приложение для планирования целей</p>

---
[![Python](https://img.shields.io/badge/python-v3.9-orange)](https://www.python.org/downloads/release/python-394/)
[![Django](https://img.shields.io/badge/django-v4.0.1-green)](https://docs.djangoproject.com/en/4.2/releases/4.0.1/)
[![Postgres](https://img.shields.io/badge/postgres-v12.4-blue)](https://www.postgresql.org/docs/12/release-12-4.html)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
___
### Как локально запустить приложение

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
BOT_TOKEN="*****"                       # Токен Telegram бота
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
### Архитектура 
![image](./infra/docker-compose.png)
___
### Краткие сведения по доступу
Для доступа к frontend-приложению нужно пройти по ссылке:  
**http://localhost:80**

**По URL backend-приложения:**

| url                                | Описание                                                                                            |
|------------------------------------|-----------------------------------------------------------------------------------------------------|
| http://localhost:8000/admin/       | Панель администрирования                                                                            |
| http://localhost:8000/core/        | Отвечает за регистрацию, авторизация и аутентификацию пользователей. Отдаёт данные о пользователях. |
| http://localhost:8000/oauth/       | Двухфакторная аутентификация                                                                        |
| http://localhost:8000/goals/       | Данные о досках, категориях, целях и их комментариях                                                |
| http://localhost:8000/bot/         | Нужен для верификация бота                                                                          |
| http://localhost:8000/docs/        | Swagger. В нем можно подробнее ознакомится доступными с роутами и их методами                       |
| http://localhost:8000/docs/schema/ | Схема Swagger`а в формате YAML                                                                      |

Для Swagger`а была выбрана библиотека [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/).
___
### Аутентификация и авторизация
С помощью frontend-приложения можно выполнить следующие функции:
- [x] регистрация,
- [x] вход/выход,
- [x] получение и обновление профиля,
- [x] смена пароля,
- [x] вход через социальную сеть VK.

Методы валидации паролей описаны в [сериализаторах](./todolist/core/serializers.py). 
Минимальная длина пароля установлена в 10 символов. 
___
### Telegram bot
Бот доступен по [ссылке](https://t.me/dlbzh_todolist_bot).
С его помощью можно создавать цели и выводить список текущих целей. 
Шаблоны сообщений выполнены при помощи Jinja2.
___
### Тесты
Тесты реализованы через [pytest-django](https://pytest-django.readthedocs.io/en/latest/). 
Сами тесты расположены в директории [/tests](./tests). Для их запуска, через командную строку в родительской дериктории (где расположен [pytest.ini](./pytest.ini)),
нужно запустить в консоли:
```shell
pytest .
```
Есть также линт тестирование проекта. Используется библиотека [ruff](https://github.com/astral-sh/ruff.git). Для запуска в консоли:
```shell
ruff check .
```
___
### Application functionality
* Вход/регистрация/аутентификация через вк.
* Создание досок.
   * Редактировани (переименование досок).
   * Шаринг досок другому пользователю.
   * Редактирование уровней доcтупа для расшариных досок (чтение, редактирование).
* Создание категорий.
* Редактирование категорий.
* Создание целей.
   * Выбор временного интервала цели с отображением кол-ва дней до завершения цели.
   * Выбор категории цели (личные, работа, развитие, спорт и т. п.) с возможностью добавлять/удалять/обновлять категории.
   * Выбор приоритета цели (статичный список minor, major, critical и т. п.).
   * Выбор статуса выполнения цели (в работе, выполнен, просрочен, в архиве). 
* Изменение целей.
   * Изменение описания цели.
   * Изменение статуса.
   * Дать возможность менять приоритет и категорию у цели.
* Удаление цели.
   * При удалении цель меняет статус на «в архиве».
* Поиск по названию цели.
* Фильтрация по статусу, категории, приоритету, году. 
* Комментарии к целям.
* Telegram бот.
   * Верификация бота.
   * Список целей с группировкой по статусу целей.
   * Создание целей.
___
