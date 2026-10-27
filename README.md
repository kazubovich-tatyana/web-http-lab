# FastAPI Notes API

Учебный проект для Innowise lab, REST API для управления заметками, построенный на FastAPI и Pydantic.

## Требования

- **Python**: 3.12 или 3.13
- **FastAPI**: 0.143.3
- **Docker**(с поддержкой Docker Compose)
- **Git**

## Быстрый старт (Развертывание проекта)

Выполните следующие команды в терминале для запуска проекта локально:

1. **Клонируйте репозиторий и перейдите в папку проекта:**
   ```bash
   git clone https://github.com/kazubovich-tatyana/web-http-lab
   cd web-http-lab
   ```
   **Создайте файл `.env` в корне проекта и укажите настройки подключения (замените на свои данные):**
    ```env
    DATABASE_URL=postgresql://your_login:your_password@localhost:5432/notes_db
    ```
---
2. **Создайте и активируйте виртуальное окружение:**
   - **Windows:**
     ```bash
     py -3.12 -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
 - **macOS / Linux:**
     ```bash
     python3.12 -m venv .venv
     source .venv/bin/activate
     ```

3. **Установите все необходимые зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
## Запуск и инициализация базы данных
В проекте используется база данных, развернутая в изолированном Docker-контейнере.

### 1. Запуск контейнера с базой данных
Чтобы поднять базу данных в фоновом режиме (демоне), выполните команду:
```bash
    docker compose up -d
```

### 2. Проверка статуса
Убедитесь, что контейнер успешно запустился и работает:
```bash
    docker compose ps
```

---
## Запуск сервера

Для запуска локального сервера разработки (Uvicorn) выполните:

```bash
   uvicorn main:app --reload
```
После запуска API будет доступно по адресу: `http://127.0.0.1:8000`
Интерактивная документация (Swagger UI): `http://127.0.0.1:8000/docs

## История Checkpoint-коммитов
| Хэш коммита | Дата | Описание чекпоинта / Что сделано 
 
4238072 | 19.10.2026 | **chore: start Notes API** авторизация приложения, создание requirements.txt, .gitignore, README.md, в main.py реализация engpoints get(/helo), get(/health)

27d987e | 20.10.2026 | **feat: add notes collection** в main.py реализация endpoints get(/notes), post(/notes)

c9967bc | 21.10.2026 | **feat: release Notes API v0.1**  main.py реализация endpoints get(/notes/{note_id}), head(/notes/{note_id}), patch(/notes/{note_id}), delete(/notes/{note_id})

хэш ком | 27.10.2026 | **feat: persist notes in postgres** подключение базы данных, создание models.py - с чистыми sql запросами, вынесение логики подлючения к бд в repasitory.py, pydantic schemas вынесены в schemas.py, реализованы endpoints для работы с пользователями