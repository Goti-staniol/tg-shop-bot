from data.cfg import db_url

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    create_engine, 
    Column,
    Integer, String, 
    Boolean,
    ForeignKey,
    Float,
    DateTime
)

engine = create_engine(db_url)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    agreement_status = Column(Boolean, default=False)
    available_balance = Column(Float, default=0)
    frozen_balacnce = Column(Float, default=0)
    block_status = Column(Boolean, default=False)
    deal_count = Column(Integer, default=0)
    positive_mark = Column(Integer, default=0)
    negative_mark = Column(Integer, default=0)
    
    comments = relationship('Comment', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')
    

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    amount = Column(Float)
    created_at = Column(DateTime, nullable=True)
    user = relationship('User', back_populates='transactions')


class MarketProduct(Base):
    __tablename__ = 'products'
    
    product_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    product_name = Column(String, nullable=False)
    product_description = Column(String, nullable=False)
    product_image = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    
    text_to_receive = Column(String, nullable=False)
    file_to_receive = Column(String, nullable=False)
    file_type = Column(String, nullable=False)

    purchase_status = Column(Boolean, default=False)
    buyer = Column(Integer, nullable=True)
    
    comments = relationship('Comment', back_populates='product')


class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    product_id = Column(String, ForeignKey(
        'products.product_id'), nullable=False)
    comment = Column(String, nullable=False)
    
    product = relationship('MarketProduct', back_populates='comments')
    user = relationship('User', back_populates='comments')