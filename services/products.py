
from datetime import datetime
from core.database import managed_transaction
from sqlalchemy.orm import Session
from models.products import Product


@managed_transaction
def get_all_products(product_id, db: Session):
    """
    Fetch all products from the database.
    """
    if not product_id:
        products = db.query(Product).all()
    else:
        products = db.query(Product).filter(Product.product_id == product_id).all()
    return products


@managed_transaction
def create_product(new_product: Product, db: Session):
    """
    Create a new product in the database.
    """
    db.add(new_product)
    return new_product


@managed_transaction
def modify_product(product_id: str, product_data, db: Session):
    """
    Modify an existing product in the database.
    """
    product = get_all_products(product_id, db=db)
    if not product:
        raise Exception(f"Product with ID {product_id} not found")
    product[0].updated_on = datetime.utcnow()
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product[0], key, value)
    return product[0]


@managed_transaction
def remove_product(product_id: str, db: Session):
    """
    Delete a product from the database.
    """
    product = db.get(Product, product_id)
    if not product:
        raise Exception(f"Product with ID {product_id} not found")
    db.delete(product)