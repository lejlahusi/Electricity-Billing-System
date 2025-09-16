# Copyright (c) 2025 Lejla Husić
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from sqlalchemy import and_, exists
from sqlalchemy.orm import Session

from . import db, schemas


def get_costumer(db_session: Session, costumer_id: str):
    """
    Retrieve a single customer by ID.

    Parameters
    ----------
    db_session : Session
        SQLAlchemy database session.
    costumer_id : str
        Unique identifier of the customer.

    Returns
    -------
    Costumer or None
        Customer record if found, otherwise None.
    """
    return db_session.query(db.Costumer).filter_by(costumer_id=costumer_id).first()

def get_costumers(db_session: Session):
    """
    Retrieve all customer records.

    Parameters
    ----------
    db_session : Session
        SQLAlchemy database session.

    Returns
    -------
    list
        List of all customer records.
    """
    return db_session.query(db.Costumer).all()

def create_costumer(db_session: Session, costumer: schemas.CostumerCreate):
    """
    Create a new customer record.

    Parameters
    ----------
    db_session : Session
        SQLAlchemy database session.
    costumer : CostumerCreate
        Pydantic schema containing customer data.

    Returns
    -------
    Costumer
        Newly created customer record.
    """
    db_costumer = db.Costumer(**costumer.dict())
    db_session.add(db_costumer)
    db_session.commit()
    db_session.refresh(db_costumer)
    return db_costumer

def create_bill(db_session: Session, costumer: schemas.BillCreate):
    """
    Create a new billing record for a customer.

    Parameters
    ----------
    db_session : Session
        SQLAlchemy database session.
    costumer : BillCreate
        Pydantic schema containing billing data.

    Returns
    -------
    Bill
        Newly created billing record.
    """
    db_bill = db.Bill(**costumer.dict())
    db_session.add(db_bill)
    db_session.commit()
    db_session.refresh(db_bill)
    return db_bill

def get_bills(db_session: Session):
    """
    Retrieve all billing records.

    Parameters
    ----------
    db_session : Session
        SQLAlchemy database session.

    Returns
    -------
    list
        List of all billing records.
    """
    return db_session.query(db.Bill).all()

def get_bill(db_session: Session, costumer_id: str,billing_month):
    """
    Retrieve a billing record for a specific customer and month.

    Parameters
    ----------
    db_session : Session
        SQLAlchemy database session.
    costumer_id : str
        Unique identifier of the customer.
    billing_month : datetime
        Month of the billing period.

    Returns
    -------
    Bill or None
        Billing record if found, otherwise None.
    """
    return db_session.query(db.Bill).filter(
        db.Bill.costumer_id == costumer_id,
        db.Bill.billing_month==billing_month

    ).first()

def create_consumption(db_session: Session, consumption: schemas.ConsumptionCreate):
    """
    Create a new consumption record if it doesn't already exist.

    Parameters
    ----------
    db_session : Session
        SQLAlchemy database session.
    consumption : ConsumptionCreate
        Pydantic schema containing consumption data.

    Returns
    -------
    Consumption
        Newly created consumption record.

    Raises
    ------
    ValueError
        If a record with the same customer ID and timestamp already exists.
    """
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
    """
    Bulk insert multiple consumption records.

    Parameters
    ----------
    db_session : Session
        SQLAlchemy database session.
    records : list of ConsumptionCreate
        List of consumption records to insert.

    Returns
    -------
    None
    """
    db_records = [db.Consumption(**record.dict()) for record in records]
    db_session.bulk_save_objects(db_records)
    db_session.commit()
