from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import date

class BatchBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    product_id: int
    supplier_id: int
    batch_number: str = Field(..., min_length=1, max_length=60)
    quantity_received: int = Field(..., gt=0)
    expiry_date: date
    received_date: date

    @model_validator(mode="after")
    def validate_expiry_after_received(self):
        if self.expiry_date <= self.received_date:
            raise ValueError("expiry_date must be later than received_date")
        return self

class BatchCreate(BatchBase):
    pass

class BatchResponse(BatchBase):
    id: int
    quantity_remaining: int

    model_config = ConfigDict(from_attributes=True)