from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ImportedData(BaseModel):
    id: Optional[UUID] = None
    random_date: Optional[date] = None
    latin_string: Optional[str] = None
    russian_string: Optional[str] = None
    even_integer: Optional[int] = None
    float_number: Optional[Decimal] = None
    file_name: Optional[str] = None
    imported_at: Optional[datetime] = None

    class Config:
        from_attributes = True
