from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import Session

from database import Base


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


def create_todo(db: Session, todo: TodoCreate) -> TodoModel:
    db_todo = TodoModel(text=todo.text, done=todo.done)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo(db: Session, todo_id: str) -> TodoModel | None:
    return db.query(TodoModel).filter(TodoModel.id == todo_id).first()


def get_todos(db: Session) -> list[TodoModel]:
    return db.query(TodoModel).all()


def update_todo(db: Session, todo_id: str, todo: TodoUpdate) -> TodoModel | None:
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    if todo.text is not None:
        db_todo.text = todo.text
    if todo.done is not None:
        db_todo.done = todo.done
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: str) -> bool:
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return False
    db.delete(db_todo)
    db.commit()
    return True
