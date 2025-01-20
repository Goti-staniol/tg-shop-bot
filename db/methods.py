from datetime import datetime, timedelta, timezone
from typing import Tuple, List, Literal, Optional, Type, Any

from sqlalchemy import delete
from sqlalchemy.orm import Session, sessionmaker

from db.models import (
    User,
    MarketProduct,
    Comment,
    Transaction,
    engine
)

def get_session() -> Session:
    session = sessionmaker(bind=engine)
    return session()

def get_user(user_id: int, session: Session) -> Type[User] | None:
    user = session.query(User).filter_by(
        user_id=user_id
    ).first()

    if user:
        return user
    return None

def get_user_by_product(product_id: str) -> int:
    with get_session() as session:
        product = session.query(MarketProduct).filter_by(
            product_id=product_id
        ).first()
        
        if product:
            return product.user_id

def add_user(user_id: int) -> None:
    with get_session() as session:
        new_user = get_user(user_id, session)
        
        if not new_user:
            session.add(User(user_id=user_id))
            session.commit()

def update_user_agreement(user_id: int) -> None:
    with get_session() as session:
        user = get_user(user_id, session)
        
        if user:
            user.agreement_status = True    
            session.commit()

def get_agreement(user_id: int) -> bool:
   with get_session() as session:
        user = get_user(user_id, session)
        if user:
            return user.agreement_status
        return False

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
    with get_session() as session:
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

def get_products() -> list[Type[MarketProduct]]:
    with get_session() as session:
        product_list = []
        products = session.query(MarketProduct).all()
        
        for product in products:
            if not product.purchase_status:
                product_list.append(product)
        
        return product_list 
    
def get_products_user(user_id: int) -> list[Type[MarketProduct]]:
    with get_session() as session:
        products = []
        user_products = session.query(MarketProduct).filter_by(
            user_id=user_id
        ).all()
        
        for product in user_products:
            products.append(product)
            
        return products

def get_product(product_id: str) -> Optional[MarketProduct]:
    with get_session() as session:
        try:
            product = session.query(MarketProduct).filter_by(
                product_id=product_id
            ).first()
            
            if product:
                return product
        except AttributeError:
            return None

def get_products_id(purchased_product: bool = True) -> List[MarketProduct]:
    with get_session() as session:
        products_id = []
        users = session.query(MarketProduct).all()
        
        for product in users:
            if not purchased_product:
                if product.buyer:
                    continue
            products_id.append(product.product_id)
        
        return products_id
    
def is_user_owner_of_product(user_id: int, product_id: str) -> bool:
    with get_session() as session:
        try:
            product = session.query(MarketProduct).filter_by(
                product_id=product_id
            ).first()
            
            if product.user_id == user_id:
                return True
            return False
        except AttributeError:
            return False

def get_purchase_status(product_id: str) -> bool:
    with get_session() as session:
        try:
            product = session.query(MarketProduct).filter_by(
                product_id=product_id
            ).first()
            
            if product.purchase_status:
                return True
            return False
        except AttributeError:
            return False

def update_product(product_id: str, user_id: int) -> None:
    with get_session() as session:
        product = session.query(MarketProduct).filter_by(
            product_id=product_id
        ).first()
        
        if product:
            product.purchase_status = True
            product.buyer = user_id
            session.commit()

def get_file_type(product_id: str) -> Literal[
    'text',
    'photo',
    'video',
    'document'
]:
    with get_session() as session:
        product = session.query(MarketProduct).filter_by(
            product_id=product_id
        ).first()
        
        return product.file_type

def add_comment_to_product(
    user_id: int, 
    product_id: str, 
    comment: str
) -> None:
    with get_session() as session:
        new_comment = Comment(
            user_id=user_id,
            product_id=product_id,
            comment=comment
        )
        session.add(new_comment)
        session.commit()


def del_comment(product_id: str) -> None:
    with get_session() as session:
        stmt = delete(Comment).filter_by(
            product_id=product_id
        )
        
        if stmt:
            session.execute(stmt)
            session.commit()

def add_mark(user_id: int, mark_type: Literal['positive', 'negative']) -> None:
    with get_session() as session:
        user = session.query(User).filter_by(user_id=user_id).first()
        
        if user:
            if mark_type == 'positive':
                user.positive_mark += 1
            if mark_type == 'negative':
                user.negative_mark += 1
            session.commit()

def deduction_mark(user_id: int, mark_type: Literal['positive', 'negative']):
    with get_session() as session:
        user = session.query(User).filter_by(user_id=user_id).first()
        
        if user:
            if mark_type == 'positive':
                user.positive_mark -= 1
            if mark_type == 'negative':
                user.negative_mark -= 1   
            session.commit()

def get_user_purchases(user_id: int) -> list[Type[MarketProduct]]:
    with get_session() as session:
        products_list = []
        products = session.query(MarketProduct).filter_by(
            buyer=user_id
        ).all()
        
        for product in products:
            products_list.append(product)
        
        return products_list

def get_user_amount(user_id: int) -> float:
    with get_session() as session:
        user = session.query(User).filter_by(
            user_id=user_id
        ).first()
        
        if user:
            return user.frozen_balacnce + user.available_balance

def balance_refill(user_id: int, amount: float | int) -> None:
    with get_session() as session:
        user = session.query(User).filter_by(
            user_id=user_id
        ).first()
        
        if user:
            user.available_balance += amount
            session.commit()

def transfer_funds(
    sender_id: int,
    recipient_id: int,
    amount_money: float | int
) -> bool:
    with get_session() as session:
        user_recipient = session.query(User).filter_by(
            user_id=recipient_id
        ).first()
        user_sender = session.query(User).filter_by(
            user_id=sender_id
        ).first()

        if user_recipient and user_sender:
            if user_sender.available_balance >= amount_money:
                user_sender.available_balance -= amount_money
                user_recipient.frozen_balacnce += amount_money
                
                transaction = Transaction(
                    user_id=recipient_id,
                    amount=amount_money,
                    created_at=datetime.now(timezone.utc)
                )
                session.add(transaction)
                session.commit()
                status = True
            else:
                status = False

        return status

def transfer_to_avaible(user_id: int) -> None:
    with get_session() as session:
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
    
def withdraw_money(user_id: int, amount: float | int) -> bool:
    with get_session() as session:
        user = session.query(User).filter_by(
            user_id=user_id
        ).first()
        
        if user and user.available_balance >= amount:
            user.available_balance -= amount
            session.commit()
            status = True
        else:
            status = False
    
        return status

def get_user_rating(user_id: int) -> tuple[Any, str]:
    with get_session() as session:
        user = session.query(User).filter_by(
            user_id=user_id
        ).first()
        
        if user:
            total_count = user.positive_mark + user.negative_mark
            if total_count != 0 and user.deal_count != 0:
                result = total_count / user.deal_count
            else:
                result = 0
            return user.deal_count, f'{result}%'
