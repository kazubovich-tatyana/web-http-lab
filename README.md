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