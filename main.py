from fastapi import FastAPI,Request,status
import models
from routers import auth,todos,admin,users
from database import engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


app=FastAPI()
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="D:/Data/Personal/Python/fastapi/TodoApp/templates")
app.mount('/static',StaticFiles(directory='D:/Data/Personal/Python/fastapi/TodoApp/static'),name='static')
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


@app.get('/')
async def test(request:Request):
    return RedirectResponse(url='/todos/todo-page',status_code=status.HTTP_302_FOUND)

