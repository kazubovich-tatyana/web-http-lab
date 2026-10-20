from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="Notes API", version="0.1.0")

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=500)

@app.get('/health')
def check_health():
  return {'status':'ok'}

@app.get('/hello')
def say_hello():
  return {"message": "Hello from Notes API"}

notes = []

@app.get('/notes')
def read_notes():
  return notes

@app.post('/notes', status_code=status.HTTP_201_CREATED)
def add_notes(note_data: NoteCreate):
  new_note = note_data.model_dump()
  new_note['id'] = len(notes)+1
  notes.append(new_note)
  return new_note