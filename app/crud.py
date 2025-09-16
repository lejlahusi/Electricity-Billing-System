# Copyright (c) 2025 Lejla Husić
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from sqlalchemy import and_, exists
from sqlalchemy.orm import Session

from . import db, schemas


def get_costumer(db_session: Session, costumer_id: str):
    return db_session.query(db.Costumer).filter_by(costumer_id=costumer_id).first()

def get_costumers(db_session: Session):
    return db_session.query(db.Costumer).all()

def create_costumer(db_session: Session, costumer: schemas.CostumerCreate):
    db_costumer = db.Costumer(**costumer.dict())
    db_session.add(db_costumer)
    db_session.commit()
    db_session.refresh(db_costumer)
    return db_costumer

def create_bill(db_session: Session, costumer: schemas.BillCreate):
    db_bill = db.Bill(**costumer.dict())
    db_session.add(db_bill)
    db_session.commit()
    db_session.refresh(db_bill)
    return db_bill

def get_bills(db_session: Session):
    return db_session.query(db.Bill).all()
def get_bill(db_session: Session, costumer_id: str,billing_month):
    return db_session.query(db.Bill).filter(
        db.Bill.costumer_id == costumer_id,
        db.Bill.billing_month==billing_month

    ).first()

def create_consumption(db_session: Session, consumption: schemas.ConsumptionCreate):
    # Check if a record with same customer_id and timestamp already exists
    exists_query = db_session.query(
        exists().where(
            and_(
                db.Consumption.costumer_id == consumption.costumer_id,
                db.Consumption.timestamp == consumption.timestamp
            )
        )
    ).scalar()

    if exists_query:
        raise ValueError("Consumption record already exists for this customer and timestamp.")

    # Proceed with insertion
    db_consumption = db.Consumption(**consumption.dict())
    db_session.add(db_consumption)
    db_session.commit()
    db_session.refresh(db_consumption)
    return db_consumption

def create_consumptions(db_session: Session, records: list[schemas.ConsumptionCreate]):
    db_records = [db.Consumption(**record.dict()) for record in records]
    db_session.bulk_save_objects(db_records)
    db_session.commit()
