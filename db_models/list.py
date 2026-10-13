from datetime import UTC, datetime
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, UniqueConstraint

from db_models.base import Base
from enums.db_enums import ListStatus


class List(Base):
  __tablename__ = 'lists'
  __table_args__ = (
      UniqueConstraint('user_id', 'anime_id', name='uq_user_anime_list'),
  )

  id = Column(Integer, primary_key=True)
  anime_id = Column(Integer, ForeignKey('anime.id'), nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  status = Column(Enum(ListStatus), nullable=False, default=ListStatus.plan_to_watch)
  created_at = Column(DateTime(timezone=True), default=datetime.now(tz=UTC))
  updated_at = Column(
      DateTime(timezone=True),
      default=datetime.now(tz=UTC),
      onupdate=datetime.now(tz=UTC),
  )

  def __init__(
      self,
      anime_id: int,
      user_id: int,
      status: ListStatus = ListStatus.plan_to_watch,
      **kwargs,
  ):
    super().__init__()
    self.anime_id = anime_id
    self.user_id = user_id
    self.status = status.value if hasattr(status, 'value') else status
    for key, value in kwargs.items():
      self.__dict__[key] = value

  def make_json(self):
    return {
        'id': self.id,
        'anime_id': self.anime_id,
        'user_id': self.user_id,
        'status': self.status.value if hasattr(self.status, 'value') else self.status,
        'created_at': self.created_at.isoformat() if self.created_at else None,
        'updated_at': self.updated_at.isoformat() if self.updated_at else None,
    }

