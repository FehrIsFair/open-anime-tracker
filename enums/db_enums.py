import enum


class AnimeType(enum.Enum):
  show = 'show'
  movie = 'movie'


class ReviewStatus(enum.Enum):
  PENDING = 'pending'
  CONFIRMED = 'confirmed'
  QUARANTINE = 'quarantined'


class SeasonType(enum.Enum):
  SEASON = 1
  ONA = 2
  OVA = 3

# def convert_string_to_anime_enum(x: str) -> AnimeType:
