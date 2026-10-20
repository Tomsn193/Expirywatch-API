# app/routers/products.py
from typing import List, cast
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import APIError
from app.models.product import Product
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


def get_product_or_404(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise APIError(
            status.HTTP_404_NOT_FOUND,
            "PRODUCT_NOT_FOUND",
            f"Product {product_id} not found",
        )
    return product


def verify_product_ownership(product: Product, current_user: User) -> None:
    if cast(int, product.owner_id) != cast(int, current_user.id):
        raise APIError(
            status.HTTP_403_FORBIDDEN,
            "FORBIDDEN",
            "You do not have access to this product",
        )


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_product = Product(owner_id=current_user.id, **product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("", response_model=List[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Product).filter(Product.owner_id == current_user.id).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_product = get_product_or_404(db, product_id)
    verify_product_ownership(db_product, current_user)
    return db_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_product = get_product_or_404(db, product_id)
    verify_product_ownership(db_product, current_user)

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_product = get_product_or_404(db, product_id)
    verify_product_ownership(db_product, current_user)

    db.delete(db_product)
    db.commit()
    return None