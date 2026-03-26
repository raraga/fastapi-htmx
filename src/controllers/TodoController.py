from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models.todo import TodoModel, TodoCreate, TodoUpdate


class TodoController:
    @staticmethod
    def create(db: Session, todo: TodoCreate) -> TodoModel:
        db_todo = TodoModel(text=todo.text, done=todo.done)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def get(db: Session, todo_id: str) -> TodoModel | None:
        return db.query(TodoModel).filter(TodoModel.id == todo_id).first()

    @staticmethod
    def get_all(db: Session) -> list[TodoModel]:
        return db.query(TodoModel).all()

    @staticmethod
    def update(db: Session, todo_id: str, todo: TodoUpdate) -> TodoModel | None:
        db_todo = TodoController.get(db, todo_id)
        if not db_todo:
            return None
        if todo.text is not None:
            db_todo.text = todo.text
        if todo.done is not None:
            db_todo.done = todo.done
        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def delete(db: Session, todo_id: str) -> bool:
        db_todo = TodoController.get(db, todo_id)
        if not db_todo:
            return False
        db.delete(db_todo)
        db.commit()
        return True


def create_todo(db: Session, todo: TodoCreate) -> TodoModel:
    return TodoController.create(db, todo)


def get_todo(db: Session, todo_id: str) -> TodoModel | None:
    return TodoController.get(db, todo_id)


def get_todos(db: Session) -> list[TodoModel]:
    return TodoController.get_all(db)


def update_todo(db: Session, todo_id: str, todo: TodoUpdate) -> TodoModel | None:
    return TodoController.update(db, todo_id, todo)


def delete_todo(db: Session, todo_id: str) -> bool:
    return TodoController.delete(db, todo_id)
