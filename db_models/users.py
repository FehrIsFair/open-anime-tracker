from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Enum, JSON, ForeignKey, DateTime
from db_models.base import Base


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  email = Column(String, nullable=False)
  password = Column(String, nullable=False)
  username = Column(String, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow())
  updated_at = Column(DateTime, default=datetime.utcnow())
  deleted_at = Column(DateTime, nullable=True)

  def __init__(self, email: str, password: str, username: str, **kwargs):
    super().__init__()
    self.email = email
    self.password = password
    self.username = username
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
