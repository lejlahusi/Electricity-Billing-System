# Copyright (c) 2025 Lejla Husić
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from datetime import datetime
from pydantic import BaseModel


class ConsumptionCreate(BaseModel):
    timestamp: datetime
    consumption: float
    price: float
    costumer_id: str

class CostumerCreate(BaseModel):
    costumer_id: str
    name: str | None = None
    email: str


class BillCreate(BaseModel):
    costumer_id: str
    name: str | None = None
    email: str
    billing_month:datetime
    billing_value:float
    billing_consumption:float