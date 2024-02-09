from sqlalchemy import Column, Integer, String, Float, Enum, JSON, ForeignKey
from db_models.base import Base


class Seasons(Base):
  __tablename__ = 'seasons'

  id = Column(Integer, primary_key=True)
  season_number = Column(Integer, nullable=False)
  anime_id = Column(Integer, ForeignKey('anime.id'), nullable=False)
  episodes = Column(Integer, nullable=False)
  desc = Column(String(255), nullable=True)
  rating = Column(Float, nullable=True)

  def __init__(self, season_number: int, anime_id: int, episodes: int, **kwargs):
    super().__init__()
    self.season_number = season_number
    self.anime_id = anime_id
    self.episodes = episodes
    for key, value in kwargs.items():
      self.__dict__[key] = value
