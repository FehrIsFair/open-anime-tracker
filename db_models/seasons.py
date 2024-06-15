from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Enum, JSON, ForeignKey, DateTime
from db_models.base import Base
from enums.db_enums import SeasonType


class Seasons(Base):
  __tablename__ = 'seasons'

  id = Column(Integer, primary_key=True)
  season_number = Column(Integer, nullable=False)
  anime_id = Column(Integer, ForeignKey('anime.id'), nullable=False)
  episodes = Column(Integer, nullable=True)
  desc = Column(String(), nullable=True)
  rating = Column(Float, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow())
  updated_at = Column(DateTime, default=datetime.utcnow())
  air_date = Column(String(), nullable=True)
  end_date = Column(String(), nullable=True)
  type_season = Column(Enum(SeasonType), nullable=False)

  def __init__(self, season_number: int, anime_id: int, episodes: int, **kwargs):
    super().__init__()
    self.season_number = season_number
    self.anime_id = anime_id
    self.episodes = episodes
    for key, value in kwargs.items():
      self.__dict__[key] = value
