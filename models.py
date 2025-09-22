from typing import Optional

from sqlalchemy import String, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class LostItem(Base):
    __tablename__ = "lost_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    lost_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    location: Mapped[str] = mapped_column(String)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="lost_items")

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    lost_items: Mapped[list["LostItem"]] = relationship("LostItem", back_populates="category")

class FoundItem(Base):
    __tablename__ = "found_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    found_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    location: Mapped[str] = mapped_column(String)
