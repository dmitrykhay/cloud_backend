# Приложение My cloud

## Структура cloud_backend:

- **auth_app - отвечает за аутентификацию, регистрацию пользователей:**
  - migrations;
  - `__init__.py`;
  - `admin.py`;
  - `apps.py`;
  - `log_in.py`;
  - `models.py`;
  - `registration.py`;
  - `serializers.py`;
  - `tests.py`;
  - `urls.py`;
  - `views.py`;
- **cloud_app - отвечает за работу с файлами:**
  - migrations;
  - `__init__.py`;
  - `admin_account.py`;
  - `admin.py`;
  - `apps.py`;
  - `is_admin_decorator`;
  - `jwt_user_id_decorator.py`;
  - `models.py`;
  - `serializers.py`;
  - `tests.py`;
  - `urls.py`;
  - `user_acciunt.py`;
  - `validate.py`;
  - `views.py`;
- **cloud_backend - содержит основные настройки сервера платформы Django framework:**
  - `__init__.py`;
  - `asgi.py`;
  - `models.py`;
  - `settings.py`;
  - `urls.py`;
  - `wsgi.py`;
- .env - содержит данные БД;
- manage.py - исполняемый модуль Django;
- README.md - содержит описание;
- requirements.txt - файл, в котором перечислены все модули, необходимые для работы проекта Django.

## Инструкция по развертыванию:

1. Установка БД Postgresql и первичная настройка:
    ```shell 
    apt install postgresql
    sudo su postgres
    psql
    ALTER USER `<имя_пользователя>` WITH PASSWORD `<пароль>`;
    CREATE DATABASE `<название_БД>`;
    \q
    exit
    ```
2. Установка серверной части приложения:
   ```shell
   - клонировать репозиторий:
        git clone https://github.com/dmitrykhay/cloud_backend.git
   - в файле cloud_backend/cloud_backend/settings.py обновить значения параметра:
    ALLOWED_HOSTS = ['<ip-адрес сервера>', 'localhost', '127.0.0.1']
   - установить зависимости:
        apt install python3
        apt install python3-pip
        apt install libpq-dev python3-dev
        python3 -m pip install psycopg2-binary
        cd cloud_backend
        pip3 install -r requirements.txt
   - выполнить миграции:
        python3 manage.py migrate
   - создать пользователя-администратора:
        python3 manage.py createsuperuser
    ```
3. Создать директорию cloud_store рядом с директорией cloud_backend.
4. Установка пользовательского интерфейса:
   ```shell
   - клонировать репозиторий:
        git clone https://github.com/dmitrykhay/cloud_frontend.git
   - установить зависимости:
        cd cloud_frontend
        apt install npm
        npm install
    ```
5. Запуск веб-приложения:
   ```shell
   - запуск серверной части:
        tmux
        cd cloud_backend
        python3 manage.py runserver 0:8000

        ctrl-b d (отключение от сессии)
   - запуск пользовательского интерфейса:
        tmux 
        cd cloud_frontend
        npm start

        ctrl-b d (отключение от сессии)
   - при необходимости зайти в процессы tmux:
        tmux ls
        tmux attach -t `<номер процесса>`
    ```
