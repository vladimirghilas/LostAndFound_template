from pydantic import BaseModel, ConfigDict
from datetime import datetime


# LostItems
class LostItemBase(BaseModel):
    category_id: int | None = None
    name: str
    description: str | None = None
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

# + легкий
# + быстрый
# - доп.запрос
# GET: /items/{id}
item = {
    "name": ...,
    "location": ...,
    "category_id": 2 # GET: /categories/2
}

# GET: /items/{id}?include=category
# - большая
# - дольше
item = {
    "name": ...,
    "location": ...,
    "category": {
        "id": 2,
        "title": "Электроника",
    }
}