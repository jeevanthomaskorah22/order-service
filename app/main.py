from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from app.models import Order
from app.database import SessionLocal  

db = SessionLocal()

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/orders")
async def get_orders():
    return db.query(Order).all()
