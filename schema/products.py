
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OfferDetails(BaseModel):
    offer: Optional[str]
    offer_type: Optional[str]
    offer_valid_till: Optional[str]
    offer_start_date: Optional[str]

class ProductCreateSchema(BaseModel):
    name: str
    description: str
    category: str
    price: float
    images: List[str]
    items: List[str]
    stock: int
    rating: Optional[float] = 0.0
    offers: Optional[OfferDetails] = None


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    images: Optional[List[str]] = None
    items: Optional[List[str]] = None
    stock: Optional[int] = None
    rating: Optional[float] = None
    offers: Optional[OfferDetails] = None


class ProductSchema(BaseModel):
    product_id: str
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]
    price: Optional[float]
    images: Optional[List[str]]
    items: Optional[List[str]]
    stock: Optional[int] = None
    rating: Optional[float] = None
    offers: Optional[OfferDetails] = None
    updated_on: Optional[datetime] = None
    created_on: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class Product(BaseModel):
    product_id: str
    name: str

    class Config:
        from_attributes = True
