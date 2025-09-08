from typing import List
from app.models import Order
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas import OrderOut, OrderCreate, OrderItemOut, OrderItemCreate
from app import crud
from app.db import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@router.post("/calculate", response_model=OrderOut)
def calculate_discount(order: OrderCreate, db: Session = Depends(get_db)):
    return crud.calculate_discount(db, order)

@router.post("/", response_model=OrderOut)
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud.place_order(db, order)

@router.get("/my", response_model=List[OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db, Order)

@router.post("/items", response_model=OrderItemOut)
def create_order_item(order_item: OrderItemCreate, db: Session = Depends(get_db)):
    return crud.create_order_item(db, order_item)

@router.get("/items/{id}", response_model=OrderItemOut)
def get_order_item(id: int, db: Session = Depends(get_db)):
    return crud.get_order_item(db, id)