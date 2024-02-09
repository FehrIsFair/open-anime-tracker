from sqlalchemy import Column, Integer, String, Float, Enum, JSON, ForeignKey
from db_models.base import Base


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  email = Column(String, nullable=False)
  password = Column(String, nullable=False)

  def __init__(self, email: str, password: str):
    super().__init__()
    self.email = email
    self.password = password
