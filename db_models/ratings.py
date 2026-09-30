from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from db_models.base import Base


class Rating(Base):
  __tablename__ = 'ratings'
  __table_args__ = (
      UniqueConstraint(
          'user_id',
          'anime_id',
          'season_id',
          postgresql_nulls_not_distinct=True,
          name='uq_user_anime_season',
      ),
  )

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  rating = Column(Integer, nullable=False)
  anime_id = Column(Integer, ForeignKey('anime.id'), nullable=False)
  season_id = Column(Integer, ForeignKey('seasons.id'), nullable=True)
  comment = Column(String(500), nullable=True)
  created_at = Column(DateTime(timezone=True), default=datetime.now(tz=UTC))
  updated_at = Column(
      DateTime(timezone=True),
      default=datetime.now(tz=UTC),
      onupdate=datetime.now(tz=UTC),
  )

  def __init__(
      self,
      user_id: int,
      rating: int,
      anime_id: int,
      season_id: int | None = None,
      comment: str | None = None,
      **kwargs,
  ):
    super().__init__()
    self.user_id = user_id
    self.rating = rating
    self.anime_id = anime_id
    self.season_id = season_id
    self.comment = comment
    for key, value in kwargs.items():
      self.__dict__[key] = value

  def make_json(self):
    return {
        'id': self.id,
        'user_id': self.user_id,
        'rating': self.rating,
        'anime_id': self.anime_id,
        'season_id': self.season_id,
        'comment': self.comment,
        'created_at': self.created_at.isoformat() if self.created_at else None,
        'updated_at': self.updated_at.isoformat() if self.updated_at else None,
    }
