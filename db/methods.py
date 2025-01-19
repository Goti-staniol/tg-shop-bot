from .models import (
    User,
    MarketProduct,
    Comment,
    Transaction,
    engine
)

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import inspect, delete

from datetime import datetime, timedelta, timezone
from typing import Tuple, List, Literal

def get_session() -> Session:
    Session = sessionmaker(bind=engine)
    return Session()

def get_user(user_id: int, session: Session) -> User:
    return session.query(User).filter(
        User.user_id == user_id
        ).first()

def get_user_by_product(product_id: str) -> int:
    session = get_session()
    product = session.query(MarketProduct).filter_by(
        product_id=product_id
    ).first()
    session.close()
    
    if product:
        return product.user_id

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
    product_to_receive: Tuple[str, str],
    file_type: str
) -> None:
    session = get_session()
    
    file_to_recieve, text_to_recieve = product_to_receive
    
    session.add(
        MarketProduct(
            product_id=product_id,
            user_id=user_id,
            product_name=product_name,
            product_description=product_description,
            product_image=product_image,
            product_price=product_price,
            text_to_receive=text_to_recieve,
            file_to_receive=file_to_recieve,
            file_type=file_type
        )
    )
    session.commit()
    session.close()

def get_products() -> List[object]:
    product_list = []
    
    session = get_session()
    products = session.query(MarketProduct).all()
    session.close()
    
    for product in products:
        if not product.purchase_status:
            product_list.append(product)
    
    return product_list 
    
def get_products_user(user_id: int) -> List[object]:
    products = []
    
    session = get_session()
    user_products = session.query(MarketProduct).filter_by(
        user_id=user_id
    ).all()
    session.close()
    
    for product in user_products:
        products.append(product)
        
    return products

def get_product(product_id: str) -> object:
    session = get_session()
    try:
        product = session.query(MarketProduct).filter_by(
            product_id=product_id
        ).first()
        
        return product
    except AttributeError:
        return None
    finally:
        session.close()

def get_products_id(purchased_product: bool = True) -> List[object]:
    products_id = []
    
    session = get_session()
    users = session.query(MarketProduct).all()
    session.close()
    
    for product in users:
        if not purchased_product:
            if product.buyer:
                continue
        products_id.append(product.product_id)
    
    return products_id
    
def is_user_owner_of_product(user_id: int, product_id: str) -> bool:
    session = get_session()
    try:
        product = session.query(MarketProduct).filter(
            MarketProduct.product_id == product_id
        ).first()
        
        if product.user_id == user_id:
            return True
        return False
    except AttributeError:
        return False
    finally:
        session.close()

def get_purchase_status(product_id: str) -> bool:
    session = get_session()
    try:
        product = session.query(MarketProduct).filter(
            MarketProduct.product_id == product_id
        ).first()
        
        if product.purchase_status:
            return True
        return False
    except AttributeError:
        return False
    finally:
        session.close()

def update_product(product_id: str, user_id: int) -> None:
    session = get_session()
    product = session.query(MarketProduct).filter_by(
        product_id=product_id
    ).first()
    
    if product:
        product.purchase_status = True
        product.buyer = user_id
        session.commit()
    session.close()

def get_file_type(product_id: str) -> Literal[
    'text',
    'photo',
    'video',
    'document'
]:
    session = get_session()
    product = session.query(MarketProduct).filter_by(
        product_id=product_id
    ).first()
    session.close()
    
    return product.file_type

def add_comment_to_product(user_id: int, product_id: str, comment: str) -> None:
    session = get_session()
    new_comment = Comment(
        user_id=user_id,
        product_id=product_id,
        comment=comment
    )
    session.add(new_comment)
    session.commit()
    session.close()

def del_comment(product_id: str) -> None:
    session = get_session()
    try:
        stmt = delete(Comment).where(Comment.product_id == product_id)
        session.execute(stmt)
        session.commit()
    finally:
        session.close()

def add_mark(user_id: int, mark: Literal['positive', 'negative']) -> None:
    session = get_session()
    user = session.query(User).filter_by(user_id=user_id).first()
    
    if user:
        if mark == 'positive':
            user.positive_mark += 1
        if mark == 'negative':
            user.negative_mark += 1
        session.commit()
    session.close()

def deduction_mark(user_id: int, mark_type: Literal['positive', 'negative']):
    session = get_session()
    user = session.query(User).filter_by(user_id=user_id).first()
    
    if user:
        if mark_type == 'positive':
            user.positive_mark -= 1
        if mark_type == 'negative':
            user.negative_mark -= 1   
        session.commit()
    session.close()

def get_user_purchases(user_id: int) -> List[object]:
    session = get_session()
    products = session.query(MarketProduct).filter_by(
        buyer=user_id
    ).all()
    session.close()
    
    return products
   
def is_buyer_of_product(user_id: int, product_id: str) -> bool:
    session = get_session()
    product = session.query(MarketProduct).filter_by(
        product_id=product_id
    ).first()
    session.close()
    
    if product.user_id == user_id:
        return True
    else:
        return False

def get_user_amount(user_id: int) -> float:
    session = get_session()
    user = session.query(User).filter_by(
        user_id=user_id
    ).first()
    session.close()
    
    if user:
        return user.frozen_balacnce + user.available_balance

def balance_refill(user_id: int, amount: float | int) -> None:
    session = get_session()
    user = session.query(User).filter_by(
        user_id=user_id
    ).first()
    
    if user:
        user.available_balance += amount
        session.commit()
    session.close()

def transfer_funds(
    sender_id: int,
    recipient_id: int,
    amount_money: float | int
) -> bool:
    session = get_session()
    users = session.query(User).filter(
        User.user_id.in_([recipient_id, sender_id])
    ).all()
    
    if users:
        user_recipient, user_sender = users
        
        if user_sender.available_balance >= amount_money:
            user_sender.available_balance -= amount_money
            user_recipient.frozen_balacnce += amount_money
            
            transaction = Transaction(
                user_id=recipient_id,
                amount=amount_money,
                created_at=datetime.now(timezone.utc)
            )
            session.add(transaction)
            status = True
        else:
            status = False
        session.commit()
    session.close()
    
    return status

def transfer_to_avaible(user_id: int) -> None:
    session = get_session()
    transactions = session.query(Transaction).filter_by(
        user_id=user_id
    ).all()
    user = session.query(User).filter_by(
        user_id=user_id
    ).first()
    
    now = datetime.now(timezone.utc)
    
    if user and transactions:
        for transaction in  transactions:
            if now - transaction.created_at >= timedelta(days=3):
                user.frozen_balacnce -= transaction.amount
                user.available_balance += transaction.amount
                session.delete(transaction)
        session.commit()
    session.close()
    
def withdraw_money(user_id: int, amount: float | int) -> bool:
    session = get_session()
    user = session.query(User).filter_by(
        user_id=user_id
    ).first()
    
    if user and user.available_balance >= amount:
        user.available_balance -= amount
        session.commit()
        
        status = True
    else:
        status = False
    session.close()
    
    return status