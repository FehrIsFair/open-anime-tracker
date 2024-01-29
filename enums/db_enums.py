import enum


class AnimeType(enum.Enum):
  SHOW = 'show'
  MOVIE = 'movie'


class ReviewStatus(enum.Enum):
  PENDING = 'pending'
  CONFIRMED = 'confirmed'
  QUARANTINE = 'quarantine'


class SeasonType(enum.Enum):
  SEASON = 1
  ONA = 2
  OVA = 3
