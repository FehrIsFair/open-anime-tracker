from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, String

from db_models.base import Base


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  email = Column(String, nullable=False)
  password = Column(String, nullable=False)
  username = Column(String, nullable=False)
  uuid = Column(String)
  created_at = Column(DateTime(timezone=True), default=datetime.now(tz=UTC))
  updated_at = Column(DateTime(timezone=True), default=datetime.now(tz=UTC))
  deleted_at = Column(DateTime(timezone=True), nullable=True)

  def __init__(self, email: str, password: str, username: str, **kwargs):
    super().__init__()
    self.email = email
    self.password = password
    self.username = username
    self.uuid = str(uuid4())
    self.set_values(**kwargs)

  def set_values(self, **kwargs):
    for key, value in kwargs.items():
      self.__dict__[key] = value

  def make_json(self):
    return_dict = {}
    for key, value in self.__dict__.items():
      match key:
        case '_sa_instance_state':
          continue
        case 'password':
          continue
        case 'email':
          continue
        case _:
          return_dict[key] = value
    return return_dict
