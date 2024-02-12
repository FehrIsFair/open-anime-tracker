from sqlalchemy import Column, Integer, String, Float, Enum, JSON, ForeignKey
from db_models.base import Base


class Rating(Base):
  __tablename__ = 'ratings'
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  rating = Column(Integer, nullable=False)
  anime_id = Column(Integer, ForeignKey('anime.id'), nullable=True)
  season_id = Column(Integer, ForeignKey('anime.id'), nullable=True)

  def __init__(self, user_id: int, rating: int, **kwargs):
    super().__init__()
    self.user_id = user_id
    self.rating = rating
    for key, value in kwargs.items():
      self.__dict__[key] = value
