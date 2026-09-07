import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from db_models.base import Base


class Invites(Base):
  __tablename__ = 'invites'
  id = Column(Integer, primary_key=True)
  uuid = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  active = Column(Boolean, nullable=False, default=True)

  def __init__(self, user_id: int):
    super().__init__()
    self.user_id = user_id
    self.uuid = uuid.uuid4()
