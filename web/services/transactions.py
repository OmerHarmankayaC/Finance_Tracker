from sqlalchemy.orm import Session
from models import Transaction
from schemas import TransactionCreate

def create_transaction(db: Session, data: TransactionCreate):
    transaction = Transaction(
        amount=data.amount,
        t_type=data.t_type,
        category=data.category,
        date=data.date,
        description=data.description
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction