from fastapi import FastAPI
from app.db import Base, engine
from app.routers import users, products, orders

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Wholesale Marketplace where you can buy and sell products with ease"}

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)

