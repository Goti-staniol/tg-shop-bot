from .models import (
    User,
    MarketProducts,
    engine
)

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import inspect
from typing import Tuple, List

def get_session() -> Session:
    Session = sessionmaker(bind=engine)
    return Session()

def get_user(user_id: int, session: Session) -> User:
    return session.query(User).filter(
        User.user_id == user_id
        ).first()

def add_user(user_id: int) -> None:
    try:
        session = get_session()
        new_user = get_user(user_id, session)
        
        if not new_user:
            session.add(User(user_id=user_id))
            session.commit()
    finally:
        session.close()

def update_user_agreement(user_id: int) -> None:
    session = get_session()
    user = get_user(user_id, session)
    
    if user:
        user.agreement_status = True    
        session.commit()
    session.close()

def get_agreement(user_id: int) -> bool:
    session = get_session()
    try:
        user = get_user(user_id, session)
        if user:
            return user.agreement_status
        return False
    finally:
        session.close()

def add_new_product(
    user_id: int,
    product_id: str,
    product_name: str,
    product_description: str | None,
    product_image: str | None,
    product_price: float | int,
    product_to_receive: Tuple[str, str]
) -> None:
    session = get_session()
    
    file_to_recieve, text_to_recieve = product_to_receive
    
    session.add(
        MarketProducts(
            product_id=product_id,
            user_id=user_id,
            product_name=product_name,
            product_description=product_description,
            product_image=product_image,
            product_price=product_price,
            text_to_receive=text_to_recieve,
            file_to_receive=file_to_recieve
        )
    )
    session.commit()
    session.close()

def get_products() -> List[object]:
    product_list = []
    
    session = get_session()
    users = session.query(MarketProducts).all()
    session.close()
    
    for user_product in users:
        product_list.append(user_product)
    
    return product_list 
    
def get_user_products(user_id: int) -> List[object]:
    products = []
    
    session = get_session()
    user_products = session.query(MarketProducts).filter_by(
        user_id=user_id
    ).all()
    session.close()
    
    for product in user_products:
        products.append(product)
        
    return products

def get_product(product_id: str) -> object:
    session = get_session()
    product = session.query(MarketProducts).filter_by(
        product_id=product_id
    ).first()
    
    return product

def get_products_id() -> None:
    products_id = []
    
    session = get_session()
    users = session.query(MarketProducts).all()
    session.close()
    
    for product in users:
        products_id.append(product.product_id)
    
    return products_id
    
def is_user_owner_of_product(user_id: int, product_id: str) -> bool:
    session = get_session()
    product = session.query(MarketProducts).filter(
        MarketProducts.product_id == product_id
    ).first()
    
    if product.user_id == user_id:
        return True
    return False
    
    
# def get_product_name(product_id: str) -> str:
#     session = get_session()
#     product = session.query(MarketProducts).filter(
#         MarketProducts.product_id == product_id
#     ).first()
    
#     session.close()
#     return product.product_name