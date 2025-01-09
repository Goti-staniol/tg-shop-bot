from data.cfg import db_url

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine, 
    Column,
    Integer, String, 
    Boolean,
    LargeBinary,
    Float
)

engine = create_engine(db_url)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    agreement_status = Column(Boolean, default=False)
    amount = Column(Float, default=0)
    block_status = Column(Boolean, default=False)


class MarketProducts(Base):
    __tablename__ = 'products'
    
    product_id = Column(String, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    product_description = Column(String, nullable=False)
    product_image = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    
    text_to_receive = Column(String, nullable=False)
    file_to_receive = Column(String, nullable=False)

    purchase_status = Column(Boolean, default=False)