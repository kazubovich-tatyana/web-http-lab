# FastAPI Notes API

Учебный проект для Innowise lab, REST API для управления заметками, построенный на FastAPI и Pydantic.

## Требования

- **Python**: 3.12 или 3.13
- **FastAPI**: 0.143.3

## Быстрый старт (Развертывание проекта)

Выполните следующие команды в терминале для запуска проекта локально:

1. **Клонируйте репозиторий и перейдите в папку проекта:**
   ```bash
   cd имя_папки_проекта
   ```
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

## Запуск сервера

Для запуска локального сервера разработки (Uvicorn) выполните:

```bash
   uvicorn main:app --reload
```
После запуска API будет доступно по адресу: `http://127.0.0.1:8000`
Интерактивная документация (Swagger UI): `http://127.0.0.1:8000/docs

Ограничение: данные хранятся в памяти и исчезают после перезапуска.

## Спецификация API (Endpoints)

#### 1. Приветственный эндпоинт
Для проверки доступности главной страницы API.

* **Method:** `GET`
* **Path:** `/hello`
* **Status (Успех):** `200 OK`

##### Пример ответа (Response Body):
```json
{
  "message": "Hello World"
}
```
---
#### 2. Проверка работоспособности (Health Check)
Используется для мониторинга состояния сервиса. Возвращает статус системы.

* **Method:** `GET`
* **Path:** `/health`
* **Status (Успех):** `200 OK`

##### Пример ответа (Response Body):
```json
{
  "status": "healthy"
}
```
---
### 3. Получение всех заметок
Возвращает полный список всех существующих заметок в виде массива. Если заметок нет, вернет пустой массив `[]`.

* **Method:** `GET`
* **Path:** `/notes`
* **Status (Успех):** `200 OK`

```json
[
  {
    "id": 1,
    "title": "note_title",
    "content": "note_content"
  },
]
```
---
### 4. Создание новой заметки
Принимает текстовые данные, автоматически генерирует уникальный целочисленный `id` и сохраняет заметку в память сервера.

* **Method:** `POST`
* **Path:** `/notes`
* **Status (Успех):** `201 Created`

#### Пример запроса (Request Body):
```json
{
  "title": "New_note",
  "content": "note_content"
}
```
#### Пример ответа (Response Body):
```json
{
  "id": 3,
  "title": "New_note",
  "content": "note_content"
}
```
---
### 5. Получение заметки по её ID
Ищет конкретную заметку в словаре по ключу `id`.

* **Method:** `GET`
* **Path:** `/notes/{note_id}` *(где `{note_id}` — целое число)*

#### Вариант А: Заметка успешно найдена
* **Status:** `200 OK`
* **Response Body:**
```json
{
  "id": 2,
  "title": "found_note",
  "content": "found_note_content"
}
```
#### Вариант Б: Заметка с таким ID не существует
* **Status:** `404 Not Found`
* **Response Body:**
```json
{
  "detail": "Note not found"
}
```
#### Вариант В: Передан некорректный ID (например, `/notes/abc`)
* **Status:** `422 Unprocessable Entity`
* **Response Body:**
```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "note_id"],
      "msg": "Input should be a valid integer...",
      "input": "abc"
    }
  ]
}
```
---
#### 6. Проверка существования заметки (HEAD)

* **Method:** `HEAD`
* **Path:** `/notes/{note_id}`
* **Успешный статус:** `200 OK`
* **Релевантные заголовки ответа:** `x-note-exists: true` 
---
#### 7. Частичное обновление (PATCH)
Изменяет только переданные поля. 

* **Method:** `PATCH`
* **Path:** `/notes/{note_id}`
* **Пример запроса (Request Body):**
  ```json
  {
    "content": "New content"
  }
  ```
* **Пример ответа при успехе (Status 200 OK):**
  ```json
  {
    "id": 1,
    "title": "Old title",
    "content": "New content"
  }
  ```
---
#### 8. Удаление ресурса (DELETE)

* **Method:** `DELETE`
* **Path:** `/notes/{note_id}`
* **Пример ответа при успехе (Status 204 No Content):**
 
## История Checkpoint-коммитов
| Хэш коммита | Дата | Описание чекпоинта / Что сделано 
 
4238072 | 19.10.2026 | **chore: start Notes API** авторизация приложения, создание requirements.txt, .gitignore, README.md, в main.py реализация engpoints get(/helo), get(/health)
27d987e | 20.10.2026 | **feat: add notes collection** в main.py реализация endpoints get(/notes), post(/notes)
        | 21.10.2026 | **feat: release Notes API v0.1** d main.py реализация endpoints get(/notes/{note_id}), head(/notes/{note_id}), patch(/notes/{note_id}), delete(/notes/{note_id})
