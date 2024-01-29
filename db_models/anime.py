from sqlalchemy import Column, Integer, String, Float, Enum, JSON
from db_models.base import Base


class Anime(Base):
  __tablename__ = 'anime'

  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False)
  jp_title = Column(String, nullable=True)
  other_titles = Column(JSON, nullable=True)
  rating = Column(Float, nullable=True)
  type = Column(Enum('show', 'movie', name='AnimeType'), nullable=False)
  seasons = Column(Integer, default=1)
  episodes = Column(Integer, default=12)
  desc = Column(String(255), nullable=True)
  status = Column(Enum('pending', 'confirmed', 'quarantine', name="ReviewStatus"), nullable=False)
