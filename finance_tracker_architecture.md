# Family Finance Tracker — Архитектура

Пет-проект для портфолио. Backend-only (без фронтенда как отдельного сервиса), запускается локально через Docker Compose, код на GitHub.

---

## Стек

- **FastAPI** — веб-фреймворк
- **PostgreSQL** — база данных (в Docker-контейнере, не облачная)
- **SQLAlchemy (async)** — ORM
- **Alembic** — миграции
- **JWT (python-jose)** — авторизация
- **Pydantic** — валидация данных
- **httpx** — асинхронные запросы к внешнему AI API (Claude/OpenAI)
- **pytest + pytest-asyncio** — тесты
- **Docker + docker-compose** — контейнеризация (FastAPI + PostgreSQL одной командой)

Никакого Streamlit, Ollama, файловой синхронизации — это учебный проект под конкретный стек резюме, не готовый продукт для реальных пользователей.

---

## Роли и логика доступа

**PARENT (родитель):**
- Создаёт аккаунты детей (привязка `child.parent_id = parent.id`)
- Вносит месячный доход семьи
- Устанавливает лимиты трат для каждого ребёнка
- Видит все покупки всех своих детей (свой кабинет — сводный список)
- НЕ может редактировать чужие покупки, только смотреть

**CHILD (ребёнок):**
- Видит только свои покупки
- Вносит покупки сам (текстовое описание + сумма)
- Видит свой остаток от лимита
- НЕ видит доход семьи и покупки других детей

Родитель тоже может внести покупку **за ребёнка** (по твоему уточнению — оба варианта). Разница на бэкенде — эндпоинт принимает `child_id` явно, и роль `PARENT` в permission-проверке имеет право указать чужой `child_id`, а `CHILD` — только свой собственный (из токена).

---

## Схема базы данных

```sql
-- Пользователи
users (
    id            SERIAL PRIMARY KEY,
    email         VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    name          VARCHAR NOT NULL,
    role          VARCHAR NOT NULL,  -- 'parent' | 'child'
    parent_id     INTEGER REFERENCES users(id) NULL,  -- NULL для родителя
    created_at    TIMESTAMP DEFAULT NOW()
)

-- Доходы семьи (вносит родитель)
incomes (
    id          SERIAL PRIMARY KEY,
    parent_id   INTEGER REFERENCES users(id),
    amount      NUMERIC(10,2) NOT NULL,
    month       DATE NOT NULL,        -- за какой месяц доход
    created_at  TIMESTAMP DEFAULT NOW()
)

-- Лимиты трат для ребёнка (устанавливает родитель)
spending_limits (
    id          SERIAL PRIMARY KEY,
    child_id    INTEGER REFERENCES users(id),
    monthly_limit NUMERIC(10,2) NOT NULL,
    month       DATE NOT NULL
)

-- Покупки
purchases (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(id),   -- кто покупатель (ребёнок)
    created_by_id   INTEGER REFERENCES users(id),   -- кто внёс запись (может быть родитель)
    description     TEXT NOT NULL,
    amount          NUMERIC(10,2) NOT NULL,
    wisdom_score    INTEGER,          -- балл осмысленности 0-100, от ИИ
    ai_comment      TEXT,             -- пояснение от ИИ
    purchased_at    TIMESTAMP DEFAULT NOW()
)
```

---

## AI-модуль: балл осмысленности

Это ключевая бизнес-логика проекта, не абстрактная классификация категорий, а оценка **рациональности конкретной траты в конкретном финансовом контексте**.

**На вход ИИ получает:**
```json
{
  "description": "Сникерс за 80р",
  "amount": 80,
  "current_balance": 100,
  "days_until_next_income": 7,
  "user_role": "child",
  "recent_spending_pattern": "3 покупки сладостей за последние 2 дня"
}
```

**Промпт примерно такой:**
```
Ты — финансовый советник для подростка. Оцени осмысленность траты
по шкале 0-100, учитывая остаток баланса и дни до следующего дохода.

Покупка: {description}, сумма {amount}₽
Остаток на балансе: {current_balance}₽
Дней до следующего пополнения: {days_until_next_income}

Верни JSON: {"score": int, "comment": "краткий совет 1-2 предложения"}
```

**Технически:**
```python
# services/ai_evaluator.py
import httpx

class PurchaseEvaluator:
    async def evaluate(self, purchase_context: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={...},
                json={"model": "claude-...", "messages": [...]}
            )
        return response.json()
```

Это даёт тебе реальный опыт **асинхронной интеграции с внешним API** — то же самое что ты уже делал в парсере с `aiohttp`, только теперь не парсинг сайта, а работа с AI API. Прямой перенос твоего существующего навыка.

---

## Структура эндпоинтов

```
POST   /auth/register          — регистрация (только родитель, дети создаются родителем)
POST   /auth/login              — получение JWT
POST   /children                — родитель создаёт аккаунт ребёнка
GET    /children                — родитель видит список своих детей

POST   /income                  — родитель вносит доход
GET    /income                  — родитель смотрит историю доходов

POST   /limits                  — родитель ставит лимит ребёнку
GET    /limits/{child_id}       — посмотреть лимит и остаток

POST   /purchases               — внести покупку (ребёнок — себе, родитель — любому своему ребёнку)
GET    /purchases               — список покупок (ребёнок видит свои, родитель — все своих детей)
GET    /purchases/{id}          — детали одной покупки с AI-оценкой

GET    /stats/summary           — сводная статистика (средний балл, топ категорий трат)
```

---

## Структура проекта

```
finance-tracker/
├── app/
│   ├── main.py
│   ├── database.py            # async engine, session
│   ├── models/
│   │   ├── user.py
│   │   ├── income.py
│   │   ├── purchase.py
│   │   └── limit.py
│   ├── schemas/                # Pydantic-схемы запросов/ответов
│   ├── routers/
│   │   ├── auth.py
│   │   ├── children.py
│   │   ├── income.py
│   │   ├── purchases.py
│   │   └── stats.py
│   ├── services/
│   │   └── ai_evaluator.py
│   ├── core/
│   │   ├── security.py         # JWT, хеширование паролей
│   │   └── permissions.py      # проверка ролей parent/child
│   └── tests/
│       ├── test_auth.py
│       ├── test_purchases.py
│       └── test_permissions.py
├── alembic/                     # миграции БД
├── docker-compose.yml            # FastAPI + PostgreSQL
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## План разработки (по неделям августа)

| Неделя | Что делаем |
|--------|-----------|
| 1 | Модели, БД, Alembic-миграции, docker-compose с PostgreSQL |
| 2 | Auth (регистрация, JWT, роли), CRUD покупок без ИИ |
| 3 | Интеграция AI-оценки, лимиты, доходы, permissions parent/child |
| 4 | pytest на ключевую логику, README, финальная полировка |

---

## Почему так, а не как предлагала другая модель

- **PostgreSQL, не SQLite** — рекрутер в финтехе ждёт именно этого в резюме
- **JWT, не файловая синхронизация** — реальный паттерн авторизации, используемый везде
- **httpx к внешнему AI API, не Ollama** — прямое продолжение твоего опыта с `aiohttp`, не новая незнакомая технология
- **Docker Compose** — запускается одной командой, это именно то что проверяют на собеседовании глядя на GitHub
