import enum


class AnimeType(enum.Enum):
  show = 'show'
  movie = 'movie'


class ReviewStatus(enum.Enum):
  pending = 'pending'
  confirmed = 'confirmed'
  quarantine = 'quarantine'


class SeasonType(enum.Enum):
  SEASON = 'season'
  ONA = 'ona'
  OVA = 'ova'
  SPECIAL = 'special'


class ListStatus(enum.Enum):
  plan_to_watch = 'plan_to_watch'
  watching = 'watching'
  complete = 'complete'
  dropped = 'dropped'
  on_hold = 'on_hold'


# def convert_string_to_anime_enum(x: str) -> AnimeType:

