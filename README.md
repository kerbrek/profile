# Profile

JSON API сервис для хранения информации о пользователе. Используется фреймворк
_FastAPI_, библиотеки _SQLAlchemy_ (async) и _Alembic_, база _PostgreSQL_.

Запускается командой `make up` и доступен по адресу <http://127.0.0.1:8000/>.

## Prerequisites

- pipenv
- make
- docker
- docker-compose

## Commands

- Start _Docker Compose_ services

  `make up`

- Setup a working environment using _Pipenv_

  `make setup`

- Start development Web server

  `make start`

- Run tests

  `make test`

- Run linter

  `make lint`

- List all available _Make_ commands

  `make help`
