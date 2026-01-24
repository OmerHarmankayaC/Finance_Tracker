from sqlalchemy import Column, Integer, Float, String
from datetime import datetime
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    t_type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    date = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
