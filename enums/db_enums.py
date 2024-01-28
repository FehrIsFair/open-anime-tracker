import enum


class AnimeType(enum.Enum):
  SHOW = 1
  MOVIE = 2


class ReviewStatus(enum.Enum):
  PENDING = 1
  CONFIRMED = 2


class SeasonType(enum.Enum):
  SEASON = 1
  ONA = 2
  OVA = 3
