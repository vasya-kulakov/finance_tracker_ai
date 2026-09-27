# Family Finance Tracker

Backend-приложение для семейного учёта финансов: родитель выдаёт лимиты и капитал детям,
дети вносят покупки, а ИИ оценивает осмысленность каждой траты.

> 🚧 Проект в активной разработке (пет-проект для портфолио). Часть эндпоинтов и ИИ-модуль
> ещё не связаны между собой — актуальный статус см. в разделе [Roadmap](#roadmap).

## Стек

- **FastAPI** — веб-фреймворк
- **PostgreSQL** + **SQLAlchemy (async)** — база данных и ORM
- **Alembic** — миграции
- **Pydantic / pydantic-settings** — валидация и конфигурация
- **pytest / pytest-asyncio** — тесты
- **Docker + docker-compose** — локальный запуск одной командой

## Быстрый старт (Docker)

Понадобится Docker и Docker Compose.

```bash
cd finance_app

# В корне проекта уже должен быть файл .env
# при необходимости отредактируйте DB_USER / DB_PASSWORD / DB_NAME

docker compose up --build
```

После старта:
- API — http://localhost:8000
- Интерактивная документация (Swagger) — http://localhost:8000/docs

При первом запуске контейнер `app` сам ждёт готовность PostgreSQL и автоматически
накатывает миграции (`alembic upgrade head`).

Если контейнеры уже были собраны ранее и вы изменили `Dockerfile`/`entrypoint.sh`,
пересоберите образ без кэша:

```bash
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up
```

### Если порт 5432 уже занят

Если на компьютере уже стоит локальный PostgreSQL, порт 5432 может быть занят, и Docker
не сможет пробросить его наружу — база и приложение всё равно поднимутся внутри
общей docker-сети. Если нужен доступ к базе с хоста, поменяй проброс порта в
`docker-compose.yml`:

```yaml
    ports:
      - "5433:5432"   # было "5432:5432"
```

## Запуск без Docker (локально)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# нужен локальный PostgreSQL и .env с DB_HOST=127.0.0.1
alembic upgrade head
uvicorn run:app --reload
```

## Переменные окружения

Файл `.env` в корне проекта:

| Переменная    | Описание                                       |
|---------------|-------------------------------------------------|
| `DB_USER`     | пользователь PostgreSQL                          |
| `DB_PASSWORD` | пароль PostgreSQL                                |
| `DB_HOST`     | хост БД (`db` в Docker, `127.0.0.1` локально)    |
| `DB_PORT`     | порт БД (обычно `5432`)                          |
| `DB_NAME`     | имя базы данных                                  |

## Основные эндпоинты

| Метод | Путь                     | Описание                                        |
|-------|--------------------------|--------------------------------------------------|
| GET   | `/`                      | приветствие / проверка, что сервис жив            |
| GET   | `/family`                | список всех пользователей (родители и дети)       |
| PUT   | `/family/add_parent`     | создать родителя                                  |
| PUT   | `/family/add_child`      | создать ребёнка (привязка к `parent_id`)          |
| POST  | `/family/{id_child}`     | начислить капитал ребёнку (по паролю родителя)    |
| POST  | `/admin/create_tables`   | создать таблицы по текущим моделям                |
| POST  | `/admin/drop_tables`     | удалить все таблицы                               |
| POST  | `/admin/reset`           | сбросить БД (drop + create)                       |
| POST  | `/run-tests`             | запустить pytest в фоне                           |
| GET   | `/test-results`          | получить результат последнего запуска тестов      |

Полный и всегда актуальный список — в Swagger (`/docs`) после запуска.

## Тесты

```bash
pytest tests/
```

либо через сам сервис (полезно, если тесты нужно погонять на уже поднятом в Docker
инстансе): `POST /run-tests`, затем `GET /test-results`.

## Структура проекта

```
finance_app/
├── run.py                  # точка входа FastAPI, роуты
├── src/
│   ├── config.py            # чтение .env через pydantic-settings
│   ├── database.py          # async engine, session, create/drop/reset
│   ├── models.py            # SQLAlchemy-модели
│   ├── repository.py        # доступ к данным (UserRepository)
│   ├── roles.py              # Pydantic-схемы Parent / Children
│   └── docs.py                # примеры JSON для Swagger
├── ai_part/                   # прототип интеграции с AI-провайдером (ZvenoAI)
├── alembic/                   # миграции БД
├── tests/                     # pytest + pytest-asyncio
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Roadmap

- [ ] Разбить `run.py` на отдельные роутеры (`auth`, `children`, `purchases`, `stats`)
- [ ] JWT-авторизация и защита `/admin/*` эндпоинтов
- [ ] Подключить AI-оценку покупок (`ai_part`) к основному API
- [ ] Лимиты трат и учёт доходов семьи
- [ ] CI (GitHub Actions) вместо ручного `/run-tests`
