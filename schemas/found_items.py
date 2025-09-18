from pydantic import BaseModel, ConfigDict
from datetime import datetime


# FoundtItems
class FoundItemBase(BaseModel):
    name: str
    description: str = None
    found_date: datetime = None
    location: str


class FoundItemCreate(FoundItemBase):
    pass


class FoundItemUpdate(BaseModel):
    name: str = None
    description: str = None
    found_date: datetime = None
    location: str = None


class FoundItem(FoundItemBase):
    id: int
