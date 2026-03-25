from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from uuid import uuid4

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Todo:
    def __init__(self, text: str):
        self.id = uuid4()
        self.text = text
        self.done = False

todos = [Todo("test")]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/todos", response_class=HTMLResponse)
async def list_todos(request: Request):
    return JSONResponse(content=jsonable_encoder(todos))
