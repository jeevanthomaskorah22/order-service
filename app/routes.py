from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.models import Order, CartItem
from app.database import SessionLocal
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

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
def create_order(
    user_id: int = Form(...),
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    new_order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Order created", "order_id": new_order.id}

@router.post("/cart")
def add_to_cart(
    user_id: int = Form(...),
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return RedirectResponse(url=f"/cart?user_id={user_id}", status_code=HTTP_302_FOUND)

@router.get("/cart", response_class=HTMLResponse)
def view_cart(
    user_id: int,
    db: Session = Depends(get_db),
    request: Request = None
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "user_id": user_id,
        "cart_items": cart_items
    })

@router.post("/cart/checkout")
def checkout_cart(
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not items:
        return {"message": "Cart is empty"}

    order_ids = []
    for item in items:
        order = Order(user_id=item.user_id, product_id=item.product_id, quantity=item.quantity)
        db.add(order)
        db.commit()
        order_ids.append(order.id)

    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
    return {"message": "Checkout complete", "order_ids": order_ids}

@router.post("/cart/remove")
def remove_item(
    cart_item_id: int = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    db.query(CartItem).filter(CartItem.id == cart_item_id).delete()
    db.commit()
    return RedirectResponse(url=f"/cart?user_id={user_id}", status_code=HTTP_302_FOUND)
