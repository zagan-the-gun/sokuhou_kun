from typing import List, Optional
from pydantic import BaseModel


class GameBase(BaseModel):
#    unique_check: Optional[str] = None
    url:         Optional[str] = None
    deadline:    Optional[str] = None
    name:        Optional[str] = None
    description: Optional[str] = None
    platform:    Optional[str] = None
    is_sent:     Optional[bool] = None
    class Config:
        orm_mode = True

class GameCreateSchema(GameBase):
    url:         Optional[str]  = None # 必須？
    deadline:    Optional[str]  = None # 必須？
    name:        Optional[str]  = None
    description: Optional[str]  = None
    platform:    Optional[str]  = None
#    is_sent:     Optional[bool] = False

class GameUpdateSchema(GameBase):
    url:         Optional[str]  = None # 必須？
    deadline:    Optional[str]  = None # 必須？
    name:        Optional[str]  = None
    description: Optional[str]  = None
    platform:    Optional[str]  = None
    is_sent:     Optional[bool] = False

class GameSchema(GameBase):
    id: int

    class Config:
        orm_mode = True

