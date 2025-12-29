from models.base_model import Base
from sqlalchemy import Column, String, TIMESTAMP, func, JSON, Float, Integer
import uuid


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_0900_ai_ci"}

    product_id = Column(String(128), primary_key=True)
    name = Column(String(100))
    description = Column(String(255))
    category = Column(String(100))
    price = Column(Float(10, 2))
    images = Column(JSON)
    items = Column(JSON)
    stock = Column(Integer)
    rating = Column(Float(2, 1), default=0.0)
    offers = Column(JSON)
    created_on = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_on = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())