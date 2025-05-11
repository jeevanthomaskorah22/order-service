from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from app.models import Order, Base
from app.database import SessionLocal  ,engine

from app.routes import router

from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db  # Import the dependency
from app.models import Order

db = SessionLocal()

app = FastAPI()
app.include_router(router)
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(router)
