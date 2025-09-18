from pydantic import BaseModel, ConfigDict
from datetime import datetime


# LostItems
class LostItemBase(BaseModel):
    name: str
    description: str = None
    lost_date: datetime = None
    location: str


class LostItemCreate(LostItemBase):
    pass


class LostItemUpdate(BaseModel):
    name: str = None
    description: str = None
    lost_date: datetime = None
    location: str = None


class LostItem(LostItemBase):
    id: int