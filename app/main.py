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
from typing import Optional  # Add this at the top


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


@app.get("/orders")
async def get_orders(order_id: Optional[int] = None, db: Session = Depends(get_db)):
    if order_id:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            return {
                "order_id": order.id,
                "user_id": order.user_id,
                "product_id": order.product_id,
                "quantity": order.quantity
            }
        else:
            return {"error": f"Order with ID {order_id} not found"}
    else:
        orders = db.query(Order).all()
        return [
            {
                "order_id": o.id,
                "user_id": o.user_id,
                "product_id": o.product_id,
                "quantity": o.quantity
            }
            for o in orders
        ]
