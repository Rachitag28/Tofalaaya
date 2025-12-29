from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Session

from models.products import Product
from core.database import get_db
from schema.products import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from services.products import get_all_products, create_product, modify_product, remove_product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductSchema])
async def get_products(product_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all products
    """
    try:
        return get_all_products(product_id, db=db)
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

@router.post("/", response_model=ProductSchema)
async def add_product(product: ProductCreateSchema, db: Session = Depends(get_db)):
    """
    Create a new product
    """
    now = datetime.utcnow()
    new_product = Product(
        **product.model_dump(),
        product_id=str(uuid4()),
        created_on=now,
        updated_on=now
    )
    try:
        create_product(new_product, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return new_product


@router.patch("/{product_id}", response_model=ProductSchema)
async def update_product(product_id: str, product_update: ProductUpdateSchema, db: Session = Depends(get_db)):
    """
    Update a product
    """
    try:
        updated_product = modify_product(product_id, product_update, db=db)
        return updated_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while updating product: {product_id}. {str(e)}"
        )
    

@router.delete("/{product_id}")
async def delete_product(product_id: str, db: Session = Depends(get_db)):
    """
    Delete a product
    """
    try:
        remove_product(product_id, db=db)
        return {"detail": f"Product with ID {product_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while deleting product: {product_id}. {str(e)}"
        )

