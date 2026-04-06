from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.setup import engine, get_db, Base
from src.models.todo import TodoCreate, TodoUpdate, TodoResponse
from src.controllers.TodoController import (
    create_todo,
    get_todo,
    get_todos,
    update_todo,
    delete_todo,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), "static")
templates = Jinja2Templates(directory="src/views")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/todos/", response_class=JSONResponse)
def list_todos(db: Session = Depends(get_db)):
    todos = get_todos(db)
    return JSONResponse(content=jsonable_encoder([TodoResponse.model_validate(t) for t in todos]))


@app.post("/todos/", response_model=TodoResponse)
def create_new_todo(request: Request, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = create_todo(db, todo)
    return TodoResponse.model_validate(db_todo)


@app.post("/todos/form", response_class=HTMLResponse)
def create_todo_form(text: str = Form(...), done: bool = Form(False), db: Session = Depends(get_db)):
    todo = TodoCreate(text=text, done=done)
    db_todo = create_todo(db, todo)
    return HTMLResponse(content="<span></span>")


@app.post("/todos/{todo_id}/toggle", response_class=HTMLResponse)
def toggle_todo(todo_id: str, db: Session = Depends(get_db)):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return HTMLResponse(content="<span>Not found</span>", status_code=404)
    todo_update = TodoUpdate(done=not db_todo.done)
    updated_todo = update_todo(db, todo_id, todo_update)
    return HTMLResponse(content="<span></span>")


@app.get("/todos/view", response_class=HTMLResponse)
def view_todos(request: Request, db: Session = Depends(get_db)):
    todos = get_todos(db)
    return templates.TemplateResponse(
        request=request,
        name="partials/todo_list.html",
        context={"todos": todos}
    )


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: str, db: Session = Depends(get_db)):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse.model_validate(db_todo)


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_existing_todo(todo_id: str, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = update_todo(db, todo_id, todo)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse.model_validate(db_todo)


@app.delete("/todos/{todo_id}")
def delete_existing_todo(todo_id: str, db: Session = Depends(get_db)):
    if not delete_todo(db, todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
