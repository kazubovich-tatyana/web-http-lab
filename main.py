from fastapi import FastAPI, status, HTTPException, Response, Depends, Query
import schemas
from db import init_db, get_db, pool
from contextlib import asynccontextmanager
from fastapi.concurrency import run_in_threadpool
import psycopg
import repository


# управление запуском и остановкой приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_in_threadpool(init_db)
    yield
    await run_in_threadpool(pool.close)


# Инициализация FastApi
app = FastAPI(title="Notes API", description='Study project, FastApi', version="0.1.0", lifespan=lifespan)


#Вся логика взаимодействия с базой вынесена в repository.py
# SQL- запросы прописаны в models.py
# Pydantic модели - schemas.py

# Работа с маршрутами.
# Проверочные endpoints
@app.get('/health')
def check_health():
  return {'status':'ok'}

@app.get('/hello')
def say_hello():
  return {"message": "Hello from Notes API"}


# endpoints для заметок

@app.post('/notes', status_code=status.HTTP_201_CREATED, response_model=schemas.NoteResponse)
def add_notes(note_data: schemas.NoteCreate, conn:psycopg.Connection=Depends(get_db)):
    try:
        new_note = repository.add_note_in_db(conn, note_data.model_dump())
        conn.commit()
        return new_note
    except ValueError as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail= str(e))


@app.get('/notes', response_model=schemas.NotePagination)
def get_notes(limit:int=Query(default = 10, ge=1, le=100),
               offset:int=Query(default=0, ge=0),
               conn:psycopg.Connection=Depends(get_db)):
    notes = repository.get_notes_in_db(conn, limit, offset)
    return notes


@app.get('/notes/{note_id}', response_model=schemas.NoteResponse)
def get_note(note_id:int, conn:psycopg.Connection=Depends(get_db)):
    try:
        note = repository.get_note_in_db(conn, note_id)
        return note
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))


@app.head('/notes/{note_id}')
def check_note(note_id:int, conn:psycopg.Connection=Depends(get_db)):
    if not repository.check_note_in_db(conn, note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return Response(status_code=status.HTTP_200_OK, headers={"x-note-exists": "true"})


@app.patch('/notes/{note_id}', response_model=schemas.NoteResponse)
def update_note(note_id:int, note_data:schemas.NoteUpdate, conn:psycopg.Connection=Depends(get_db)):
    update_fields = note_data.model_dump(exclude_unset=True)
    if not update_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="all fields are empty")

    try:
        note = repository.update_note_in_db(conn, note_id, update_fields)
        conn.commit()
        return note
    except LookupError as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete('/notes/{note_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_note(note_id:int, conn:psycopg.Connection=Depends(get_db)):
    try:
        repository.delete_note_in_db(conn, note_id)
    except LookupError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))
    return Response(status_code = status.HTTP_204_NO_CONTENT)



# endpoints для пользователей

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def add_user(user_data:schemas.UserCreate, conn:psycopg.Connection=Depends(get_db)):
    try:
        user = repository.add_user_in_db(conn, user_data.model_dump())
        return user
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))


@app.head('/users/{user_id}')
def check_user(user_id:int, conn:psycopg.Connection=Depends(get_db)):
    if repository.check_user_in_db(conn, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_200_OK, headers={"x-user-exists": "true"})


@app.get('/users/{user_id}', response_model=schemas.UserResponse)
def get_user(user_id:int, conn:psycopg.Connection=Depends(get_db)):
    try:
        user = repository.get_user_in_db(conn, user_id)
        return user
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = str(e))


@app.get('/users/{user_id}/notes', response_model=schemas.NotePagination)
def get_user_notes(user_id:int,
                   limit:int=Query(default = 10, ge=1, le=100),
                   offset:int=Query(default=0, ge=0),
                   conn:psycopg.Connection=Depends(get_db)):
    try:
        notes = repository.get_user_notes_in_db(conn, user_id, limit, offset)
        return notes
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))


@app.delete('/users/{user_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int, conn:psycopg.Connection=Depends(get_db)):
    try:
        repository.delete_user_in_db(conn, user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = str(e))