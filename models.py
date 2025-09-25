from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sqlalchemy import Table

lost_item_tags = Table(
    "lost_item_tags",
    Base.metadata,
    Column("lost_item_id", ForeignKey("lost_items.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

found_item_tags = Table(
    "found_item_tags",
    Base.metadata,
    Column("found_item_id", ForeignKey("found_items.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)
class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    lost_items: Mapped[list["LostItem"]] = relationship(
        secondary=lambda: lost_item_tags,
        back_populates="tags"
    )
    found_items: Mapped[list["FoundItem"]] = relationship(
        secondary=lambda: found_item_tags,
        back_populates="tags"
    )

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    lost_items: Mapped[list["LostItem"]] = relationship(back_populates="category")


class LostItem(Base):
    __tablename__ = "lost_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    lost_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    location: Mapped[str] = mapped_column(String)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[Optional["Category"]] = relationship(back_populates="lost_items")

    tags: Mapped[list[Tag]] = relationship(
        secondary=lambda: lost_item_tags,
        back_populates="lost_items"
    )

class FoundItem(Base):
    __tablename__ = "found_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    found_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    location: Mapped[str] = mapped_column(String)

    tags: Mapped[list[Tag]] = relationship(
        secondary=lambda : found_item_tags,
        back_populates="found_items"
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, index=True, default=None)
    full_name: Mapped[Optional[str]] = mapped_column(String, default=None)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())