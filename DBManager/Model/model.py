from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String


class Base(DeclarativeBase): pass 

class Item(Base):
    __tablename__ = "ItemsMV"

    productId = Column(Integer, primary_key=True)
    name = Column(String)
    basePrice = Column(Integer)
    salePrice = Column(Integer)
    bonusRubles = Column(Integer)
    linkToproduct = Column(String)

class Image(Base):
    __tablename__ = "Images"
    
    id = Column(Integer, primary_key=True, index=True)
    productId = Column(Integer)
    pathImage = Column(String)