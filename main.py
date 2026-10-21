from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Notes API", version="0.1.0")

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=500)

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=80)
    content: Optional[str] = Field(default=None, min_length=1, max_length=500)


@app.get('/health')
def check_health():
  return {'status':'ok'}

@app.get('/hello')
def say_hello():
  return {"message": "Hello from Notes API"}

notes = {}

@app.get('/notes')
def read_notes():
  return list(notes.values())

@app.post('/notes', status_code=status.HTTP_201_CREATED)
def add_notes(note_data: NoteCreate):
  current_id = max(notes.keys()) + 1 if len(notes.keys()) > 0 else 1
  new_note = note_data.model_dump()
  new_note['id'] = current_id
  notes[current_id] = new_note
  return new_note

@app.get('/notes/{note_id}')
def get_note(note_id:int):
    note = notes.get(note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

@app.head('/notes/{note_id}')
def check_note(note_id:int):
    note = notes.get(note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return Response(status_code=status.HTTP_200_OK, headers={"x-note-exists": "true"})

@app.patch('/notes/{note_id}')
def update_note(note_id:int, note_data:NoteUpdate):
    note = notes.get(note_id)
    if note is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Note not found')
    note.update(note_data.model_dump(exclude_unset=True))
    notes[note_id] = note
    return note

@app.delete('/notes/{note_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_note(note_id:int):
    if not (note_id in notes):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Note not found')
    del notes[note_id]
    return Response(status_code = status.HTTP_204_NO_CONTENT)

