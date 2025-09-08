from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas import ProductOut, ProductCreate
from app import crud
from app.db import get_db

router = APIRouter(prefix="/products", tags=["Products"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)
    
@router.get("/{id}", response_model=ProductOut)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_product_by_id(db, id)