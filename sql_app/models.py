from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Game(Base):
    __tablename__ = "games"

    id           = Column(Integer, primary_key=True, index=True)
    url          = Column(String)
    deadline     = Column(String) # 同じゲームを同じURLで数ヶ月後に再配布する場合もあるのでdateで区別を付ける
    name         = Column(String, index=True)
    description  = Column(String, index=True)
    platform     = Column(String, index=True)
    is_sent      = Column(Boolean, default=False)

