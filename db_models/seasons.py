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
