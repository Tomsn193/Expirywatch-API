from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class StockAdjustment(Base):
    __tablename__ = "stock_adjustments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    quantity_change = Column(Integer, nullable=False)
    reason = Column(String(30), nullable=False)
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    batch = relationship("Batch", back_populates="adjustments")

    __table_args__ = (
        CheckConstraint("quantity_change != 0", name="ck_adj_quantity_change_nonzero"),
        CheckConstraint(
            "reason IN ('sold', 'damaged', 'expired', 'correction')", 
            name="ck_adj_reason_valid"
        ),
        CheckConstraint(
            "(reason = 'correction') OR (quantity_change < 0)", 
            name="ck_adj_reason_logic"
        ),
    )