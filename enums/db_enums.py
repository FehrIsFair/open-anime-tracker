import enum


class AnimeType(enum.Enum):
  show = 'show'
  movie = 'movie'


class ReviewStatus(enum.Enum):
  PENDING = 'pending'
  CONFIRMED = 'confirmed'
  QUARANTINE = 'quarantine'


class SeasonType(enum.Enum):
  SEASON = 'season'
  ONA = 'ona'
  OVA = 'ova'

# def convert_string_to_anime_enum(x: str) -> AnimeType:
