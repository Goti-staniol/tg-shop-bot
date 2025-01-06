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
    

class MarketProducts(Base):
    __tablename__ = 'products'
    
    user_id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    prodct_discription = Column(String, nullable=False)
    product_image = Column(LargeBinary, nullable=False)
    product_price = Column(Float, nullable=False)
    
