from pydantic import BaseModel
from datetime import datetime


# LostItems
class LostItemBase(BaseModel):
    category_id: int | None = None
    name: str
    description: str | None = None
    lost_date: datetime | None = None
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