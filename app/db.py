# Copyright (c) 2025 Lejla Husić
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///elektricna_energija.db')

Session= sessionmaker(bind=engine)
session=Session()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Consumption(Base):
    """
    SQLAlchemy model for electricity consumption records.

    Attributes
    ----------
    id : int
        Primary key.
    timestamp : datetime
        Timestamp of the consumption measurement.
    consumption : float
        Amount of electricity consumed in kWh.
    price : float
        Price per kWh in EUR.
    costumer_id : str
        Foreign key referencing the customer.
    """
    __tablename__='electrical_constumption'
    id=Column(Integer, primary_key=True, index=True)
    timestamp=Column(DateTime, index=True)
    consumption=Column(Float, nullable=False)
    price=Column(Float, nullable=False)
    costumer_id=Column(String, ForeignKey("costumers.costumer_id"))

class Costumer(Base):
    """
    SQLAlchemy model for customer records.

    Attributes
    ----------
    costumer_id : str
        Primary key and unique identifier for the customer.
    name : str or None
        Full name of the customer.
    email : str
        Email address of the customer.
    """
    __tablename__='costumers'
    costumer_id=Column(String,primary_key=True, nullable=False)
    name=Column(String, nullable=True)
    email=Column(String, nullable=False)


class Bill(Base):
    """
    SQLAlchemy model for billing records.

    Attributes
    ----------
    costumer_id : str
        Primary key and customer identifier.
    name : str or None
        Full name of the customer.
    email : str
        Email address of the customer.
    billing_month : datetime
        Month for which the bill is generated.
    billing_value : float
        Total billing amount in EUR.
    billing_consumption : float
        Total electricity consumption in kWh.
    """
    __tablename__='bills'
    costumer_id=Column(String,primary_key=True, nullable=False)
    name=Column(String, nullable=True)
    email=Column(String, nullable=False)
    billing_month=Column(DateTime, index=True)
    billing_value=Column(Float, nullable=False)
    billing_consumption=Column(Float, nullable=False)


Base.metadata.create_all(bind=engine)

    

