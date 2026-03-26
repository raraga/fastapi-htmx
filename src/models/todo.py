from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime

from database.setup import Base


class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    text = Column(String, nullable=False)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TodoBase(BaseModel):
    text: str
    done: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    text: str | None = None
    done: bool | None = None


class TodoResponse(TodoBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
