from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    t_type: str
    category: str
    date: str
    description: str | None = None

class TransactionCreate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True
