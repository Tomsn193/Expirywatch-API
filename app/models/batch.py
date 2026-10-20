from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    batch_number = Column(String(60), nullable=False)
    quantity_received = Column(Integer, nullable=False)
    quantity_remaining = Column(Integer, nullable=False)
    expiry_date = Column(Date, nullable=False)
    received_date = Column(Date, nullable=False)

    # Relationships
    product = relationship("Product", backref="batches")
    supplier = relationship("Supplier", back_populates="batches")
    adjustments = relationship("StockAdjustment", back_populates="batch")

    __table_args__ = (
        Index("uix_supplier_batch", "supplier_id", "batch_number", unique=True),
        CheckConstraint("quantity_received > 0", name="ck_batches_quantity_received_positive"),
        CheckConstraint("quantity_remaining >= 0", name="ck_batches_quantity_remaining_nonnegative"),
    )