from sqlalchemy.orm import Session
from web import models, schemas

def create_transaction(db: Session, data: schemas.TransactionCreate):
    transaction = models.Transaction(
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

def update_transaction(db: Session, transaction_id: int, transaction_update: schemas.TransactionUpdate):
    transaction = (db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first())

    if not transaction:
        return None
    
    update_data = transaction_update.model_dump(exclude_unset = True)

    for field, value in update_data.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)

    return transaction