from sqlalchemy import Column, Integer, String, Float, Enum, JSON, ForeignKey
from db_models.base import Base


class List(Base):
  __tablename__ = 'lists'
  id = Column(Integer, primary_key=True)
  anime_id = Column(Integer, ForeignKey('anime.id'), nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

  def __init__(self, anime_id: int, user_id: int):
    super().__init__()
    self.anime_id = anime_id
    self.user_id = user_id
