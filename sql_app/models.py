from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Game(Base):
    __tablename__ = "games"

    id           = Column(Integer, primary_key=True, index=True)
    unique_check = Column(String, unique=True, index=True) # url + dateでユニークチェック
    url          = Column(String)
    #date        = Column(DateTime)
    date         = Column(String)
    name         = Column(String, index=True)
    description  = Column(String, index=True)
    platform     = Column(String, index=True)
    delivery     = Column(Boolean, default=False)
