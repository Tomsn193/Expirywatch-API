from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import APIError
from app.models.batch import Batch
from app.models.product import Product
from app.models.adjustment import StockAdjustment
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.adjustment import AdjustmentCreate, AdjustmentResponse

router = APIRouter(prefix="/batches", tags=["Stock Adjustments"])

@router.post("/{batch_id}/adjustments", response_model=AdjustmentResponse, status_code=status.HTTP_201_CREATED)
def create_adjustment(
    batch_id: int,
    payload: AdjustmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Lock the batch row until commit or rollback
    batch = (
        db.query(Batch)
        .join(Product)
        .filter(Batch.id == batch_id)
        .with_for_update()
        .first()
    )

    if not batch:
        db.rollback()
        raise APIError(status.HTTP_404_NOT_FOUND, "BATCH_NOT_FOUND", f"Batch {batch_id} not found")

    # Check ownership via the parent product
    if batch.product.owner_id != current_user.id:
        db.rollback()
        raise APIError(status.HTTP_403_FORBIDDEN, "FORBIDDEN", "You do not have access to this batch")

    new_remaining = batch.quantity_remaining + payload.quantity_change
    if new_remaining < 0: # type: ignore
        db.rollback()
        raise APIError(status.HTTP_409_CONFLICT, "INSUFFICIENT_STOCK", "Adjustment would make stock negative")

    adjustment = StockAdjustment(
        batch_id=batch.id,
        quantity_change=payload.quantity_change,
        reason=payload.reason,
        note=payload.note
    )
    batch.quantity_remaining = new_remaining # type: ignore
    db.add(adjustment)
    db.commit()
    db.refresh(adjustment)
    return adjustment

@router.get("/{batch_id}/adjustments", response_model=List[AdjustmentResponse])
def get_adjustments(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    batch = db.query(Batch).join(Product).filter(Batch.id == batch_id).first()
    
    if not batch:
        raise APIError(status.HTTP_404_NOT_FOUND, "BATCH_NOT_FOUND", "Batch not found")
    if batch.product.owner_id != current_user.id:
        raise APIError(status.HTTP_403_FORBIDDEN, "FORBIDDEN", "You do not have access to this batch")

    return db.query(StockAdjustment).filter(StockAdjustment.batch_id == batch_id).order_by(StockAdjustment.created_at).all()