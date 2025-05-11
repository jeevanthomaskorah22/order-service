from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Order
from app.database import get_db
from pydantic import BaseModel
import requests

router = APIRouter()

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        # Placeholder for future product service integration
        # response = requests.get(f"http://product-service/products/{order.product_id}")
        # response.raise_for_status()
        pass
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Product service unavailable")

    new_order = Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Order created", "order_id": new_order.id}

@router.get("/orders")
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    enriched_orders = []
    for order in orders:
        try:
            # Future: Replace with actual product service URL
            # product_resp = requests.get(f"http://product-service/products/{order.product_id}")
            # product_resp.raise_for_status()
            # product_data = product_resp.json()

            # Simulate product data for now
            product_data = {
                "name": f"Product-{order.product_id}",
                "description": "Placeholder description"
            }
        except:
            product_data = {"error": "Product service unavailable"}

        enriched_orders.append({
            "id": order.id,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "status": order.status,
            "created_at": order.created_at,
            "product": product_data
        })

    return enriched_orders
