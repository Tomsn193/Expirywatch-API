from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import APIError
from app.models.batch import Batch
from app.models.product import Product
from app.models.supplier import Supplier
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.batch import BatchCreate, BatchResponse

router = APIRouter(prefix="/batches", tags=["Batches"])


@router.post("", response_model=BatchResponse, status_code=status.HTTP_201_CREATED)
def create_batch(
    payload: BatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Verify the product exists and belongs to the user
    product = db.query(Product).filter(
        Product.id == payload.product_id, Product.owner_id == current_user.id
    ).first()
    if not product:
        raise APIError(status.HTTP_400_BAD_REQUEST, "INVALID_REFERENCE", "Invalid product reference")

    # 2. Verify the supplier exists and belongs to the user
    supplier = db.query(Supplier).filter(
        Supplier.id == payload.supplier_id, Supplier.owner_id == current_user.id
    ).first()
    if not supplier:
        raise APIError(status.HTTP_400_BAD_REQUEST, "INVALID_REFERENCE", "Invalid supplier reference")

    # 3. Check for duplicate batch number for this supplier
    existing_batch = db.query(Batch).filter(
        Batch.supplier_id == payload.supplier_id,
        Batch.batch_number == payload.batch_number
    ).first()
    if existing_batch:
        raise APIError(status.HTTP_409_CONFLICT, "DUPLICATE_BATCH", "Batch number already exists for this supplier")

    # 4. Create batch. quantity_remaining starts equal to quantity_received.
    batch = Batch(
        **payload.model_dump(),
        quantity_remaining=payload.quantity_received
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


@router.get("", response_model=List[BatchResponse])
def list_batches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Join with Product to ensure we only list batches belonging to this user's products
    return db.query(Batch).join(Product).filter(Product.owner_id == current_user.id).all()


# MUST be declared before /{batch_id} to prevent routing conflicts
@router.get("/expiring-soon", response_model=List[BatchResponse])
def get_expiring_soon(
    days: int = Query(30, ge=0, le=365, description="Number of days to look ahead for expiring batches"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    future_date = today + timedelta(days=days)

    return (
        db.query(Batch)
        .join(Product)
        .filter(
            Product.owner_id == current_user.id,
            Batch.quantity_remaining > 0,           # Exclude zero-stock batches
            Batch.expiry_date >= today,             # Exclude already expired batches
            Batch.expiry_date <= future_date        # Within the requested timeframe
        )
        .all()
    )


@router.get("/{batch_id}", response_model=BatchResponse)
def get_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise APIError(status.HTTP_404_NOT_FOUND, "BATCH_NOT_FOUND", f"Batch {batch_id} not found")
    
    if batch.product.owner_id != current_user.id:
        raise APIError(status.HTTP_403_FORBIDDEN, "FORBIDDEN", "You do not have access to this batch")
        
    return batch