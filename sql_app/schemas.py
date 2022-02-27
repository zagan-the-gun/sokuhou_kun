from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    unique_check: Optional[str] = None
    url: Optional[str] = None
    date: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    platform: Optional[str] = None
#    delivery: bool
    delivery: Optional[bool] = None


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    pass


class Game(GameBase):
    id: int

    class Config:
        orm_mode = True

