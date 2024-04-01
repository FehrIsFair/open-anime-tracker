import pdb
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Enum, JSON, DateTime, Boolean

from db_models.base import Base
from enums.db_enums import AnimeType, ReviewStatus


class Anime(Base):
  __tablename__ = 'anime'

  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False)
  jp_title = Column(String, nullable=True)
  other_titles = Column(JSON, nullable=True)
  rating = Column(Float, nullable=True)
  _type = Column(Enum(AnimeType), nullable=False)
  seasons = Column(Integer, default=1)
  episodes = Column(Integer, default=12, nullable=True)
  desc = Column(String(), nullable=True)
  status = Column(Enum(ReviewStatus), nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow())
  updated_at = Column(DateTime, default=datetime.utcnow())
  rank = Column(Integer, nullable=True)
  content_rating = Column(String(), default='PG')
  nsfw = Column(Boolean, default=False)

  def __init__(self, title:str, _type: AnimeType, status: ReviewStatus = ReviewStatus.pending, **kwargs):
    super().__init__()
    self.title = title
    self._type = _type
    self.status = status.value
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
        case '_type':
          return_dict[key] = value.value
        case 'status':
          return_dict[key] = value.value
        case _:
          return_dict[key] = value
    return return_dict
