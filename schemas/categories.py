from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str = ""


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
