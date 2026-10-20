from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import APIError
from app.models.supplier import Supplier
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

def get_supplier_or_404(db: Session, supplier_id: int) -> Supplier:
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier is None:
        raise APIError(
            status.HTTP_404_NOT_FOUND,
            "SUPPLIER_NOT_FOUND",
            f"Supplier {supplier_id} not found",
        )
    return supplier

def verify_supplier_ownership(supplier: Supplier, current_user: User) -> None:
    if int(supplier.owner_id) != int(current_user.id): # type: ignore
        raise APIError(
            status.HTTP_403_FORBIDDEN,
            "FORBIDDEN",
            "You do not have access to this supplier",
        )

@router.post("", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    payload: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    supplier = Supplier(owner_id=current_user.id, **payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

@router.get("", response_model=List[SupplierResponse])
def list_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Supplier).filter(Supplier.owner_id == current_user.id).all()

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    supplier = get_supplier_or_404(db, supplier_id)
    verify_supplier_ownership(supplier, current_user)
    return supplier

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    payload: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    supplier = get_supplier_or_404(db, supplier_id)
    verify_supplier_ownership(supplier, current_user)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(supplier, key, value)

    db.commit()
    db.refresh(supplier)
    return supplier

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    supplier = get_supplier_or_404(db, supplier_id)
    verify_supplier_ownership(supplier, current_user)

    # Prevent deleting suppliers referenced by batches
    if supplier.batches:
        raise APIError(
            status.HTTP_409_CONFLICT,
            "SUPPLIER_HAS_BATCHES",
            "Cannot delete supplier with active batches",
        )

    db.delete(supplier)
    db.commit()
    return None