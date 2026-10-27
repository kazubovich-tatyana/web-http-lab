from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

# Create Enum for status
# -----------------------------------------
class NoteStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    REVIEWED = "reviewed"

# schemas for users
# ------------------------------------------

class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

# schemas for notes
#-----------------------------------------------------
class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=500)
    status: Optional[NoteStatus] = NoteStatus.DRAFT
    user_id: int

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    status: NoteStatus
    time_created: datetime
    user_id: int

class NotePagination(BaseModel):
    total: int
    limit: int
    offset: int
    notes: list[NoteResponse]

class NoteUpdate(BaseModel):
    id: Optional[int] = Field(default=None)
    title: Optional[str] = Field(default=None, min_length=1, max_length=80)
    content: Optional[str] = Field(default=None, min_length=1, max_length=500)
    status: Optional[NoteStatus] = Field(default=None)
    user_id: Optional[int] = Field(default=None)

