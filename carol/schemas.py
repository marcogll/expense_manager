from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class MacroCategory(str, Enum):
    PERSONAL = "Personal"
    BUSINESS = "Negocio"


class Item(BaseModel):
    name: str
    quantity: int = 1
    unit_price: float
    total: float
    subcategory: Optional[str] = None


class Transaction(BaseModel):
    store: str
    rfc: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    folio: Optional[str] = None
    date: str
    time: Optional[str] = None
    total: float
    currency: str = "MXN"
    macro: MacroCategory
    subcategory: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    items: List[Item] = []
    raw_text: Optional[str] = None
    registered_at: str = Field(default_factory=lambda: datetime.now().isoformat())
