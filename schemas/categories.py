from typing import Optional
from pydantic import BaseModel, ConfigDict
from .lost_items import LostItem

class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryRead(CategoryBase):
    id: int
    lost_item: list["LostItem"] = []
    model_config = ConfigDict(from_attributes=True)
    