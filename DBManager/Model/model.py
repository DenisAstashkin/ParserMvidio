from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, LargeBinary


class Base(DeclarativeBase): pass 

class Item(Base):
    __tablename__ = "ItemsMV"

    productId = Column(Integer, primary_key=True)
    name = Column(String)
    basePrice = Column(Integer)
    salePrice = Column(Integer)
    bonusRubles = Column(Integer)
    linkToproduct = Column(String)
    image = Column(LargeBinary)
