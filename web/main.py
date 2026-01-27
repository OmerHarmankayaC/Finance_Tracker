from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from web.schemas import TransactionUpdate, TransactionOut, TransactionCreate
from web.services.transactions import update_transaction

from web.database import Base, engine, get_db
from web.models import Transaction


app = FastAPI(title="Finance Tracker API")

Base.metadata.create_all(bind=engine)


@app.post("/transactions", response_model = TransactionOut)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    if transaction.t_type not in ("income", "expense"):
        raise HTTPException(status_code = 400, detail = "t_type must be income or expense")

    if transaction.amount <= 0:
        raise HTTPException(status_code = 400, detail = "amount must be positive")

    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


@app.get("/transactions", response_model = list[TransactionOut])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()


@app.get("/transactions/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code = 404, detail = "Transaction not found")

    return transaction


@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code = 404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted"}

@app.patch("/transactions/{transaction_id}", response_model = TransactionOut)
def update_transaction_api(transaction_id: int, transation_update: TransactionUpdate, db: Session = Depends(get_db)):
    updated = update_transaction(db, transaction_id, transation_update)

    if not updated:
        raise HTTPException(status_code = 404, detail = "Transaction not found")
    
    return updated
