from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime
from typing import Optional

class AdjustmentBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    quantity_change: int = Field(..., description="Must not be zero")
    reason: str = Field(..., description="sold, damaged, expired, or correction")
    note: Optional[str] = Field(None, max_length=255)

    @model_validator(mode="after")
    def validate_reason_and_quantity(self):
        if self.quantity_change == 0:
            raise ValueError("quantity_change cannot be zero")
        if self.reason not in ["sold", "damaged", "expired", "correction"]:
            raise ValueError("Invalid reason")
        if self.reason in ["sold", "damaged", "expired"] and self.quantity_change > 0:
            raise ValueError(f"reason '{self.reason}' requires a negative quantity_change")
        return self

class AdjustmentCreate(AdjustmentBase):
    pass

class AdjustmentResponse(AdjustmentBase):
    id: int
    batch_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)