# Copyright (c) 2025 Lejla Husić
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from datetime import datetime
from pydantic import BaseModel


class ConsumptionCreate(BaseModel):
    """
    Schema for creating a consumption record.

    Attributes
    ----------
    timestamp : datetime
        Timestamp of the consumption measurement.
    consumption : float
        Amount of electricity consumed in kWh.
    price : float
        Dynamic price per kWh in EUR.
    costumer_id : str
        Unique identifier of the customer.
    """
    timestamp: datetime
    consumption: float
    price: float
    costumer_id: str

class CostumerCreate(BaseModel):
    """
    Schema for creating a customer record.

    Attributes
    ----------
    costumer_id : str
        Unique identifier of the customer.
    name : str or None, optional
        Full name of the customer.
    email : str
        Email address of the customer.
    """
    costumer_id: str
    name: str | None = None
    email: str


class BillCreate(BaseModel):
    """
    Schema for creating a billing record.

    Attributes
    ----------
    costumer_id : str
        Unique identifier of the customer.
    name : str or None, optional
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
    costumer_id: str
    name: str | None = None
    email: str
    billing_month:datetime
    billing_value:float
    billing_consumption:float