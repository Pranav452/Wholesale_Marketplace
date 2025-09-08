from sqlalchemy.orm import Session
from app.models import User, Product, Order, OrderItem
from app.schemas import UserCreate, ProductCreate, OrderCreate, OrderItemCreate
from app.auth.hashing import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
    
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_pw, username=user.username, created_at=user.created_at, user_type=user.user_type, company_name=user.company_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_product(db: Session, product: ProductCreate):
    'Add a product to the database'
    db_product = Product(vendor_id=product.vendor_id, name=product.name, category=product.category, price=product.price, min_quantity=product.min_quantity, stock=product.stock, created_at=product.created_at)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    'Get all products from the database'
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    'Get a product by id'
    return db.query(Product).filter(Product.id == product_id).first()
def calculate_discount(db: Session, order: OrderCreate):

    total_quantity = sum(order_item.quantity for order_item in order.order_items)
    bonus_discount = 0
    if total_quantity >= 1000:
        bonus_discount = 0.05
    elif total_quantity >= 5000:
        bonus_discount = 0.1
    elif total_quantity >= 10000:
        bonus_discount = 0.15
    else:
        bonus_discount = 0
    total_value = sum(order_item.unit_price * order_item.quantity for order_item in order.order_items)
    value_discount = 0
    if total_value >= 1000:
        value_discount = 0.03
    elif total_value >= 5000:
        value_discount = 0.07
    elif total_value >= 10000:
        value_discount = 0.12
    else:
        value_discount = 0
    loyalty_discount = 0
    orders_count = db.query(Order).filter(Order.buyer_id == order.buyer_id).count()
    if orders_count >= 1 and orders_count <= 3:
        loyalty_discount = 0.02
    elif orders_count >= 4:
        loyalty_discount = 0.05
    else:
        loyalty_discount = 0
    total_discount = bonus_discount + value_discount + loyalty_discount
    if total_discount > 0.25:
        total_discount = 0.25
    return total_discount

def place_order(db: Session, order: OrderCreate):
    'Place order with discount'
    discount = calculate_discount(db, order)
    order.discount_percent = discount
    order.final_amount = order.total_amount - (order.total_amount * discount)
    db_order = Order(buyer_id=order.buyer_id, total_amount=order.total_amount, discount_percent=order.discount_percent, final_amount=order.final_amount, created_at=order.created_at)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, buyer_id: int):
    'Get user\'s orders'
    return db.query(Order).filter(Order.buyer_id == buyer_id)

def create_order_item(db: Session, order_item: OrderItemCreate):
    'Create an order item'
    db_order_item = OrderItem(order_id=order_item.order_id, product_id=order_item.product_id, quantity=order_item.quantity, unit_price=order_item.unit_price, subtotal=order_item.subtotal, created_at=order_item.created_at)
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

def get_order_item(db: Session, id: int):
    'Get an order item by id'
    return db.query(OrderItem).filter(OrderItem.id == id).first()


