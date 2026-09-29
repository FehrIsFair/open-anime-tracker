from datetime import date, datetime, timedelta, timezone
from sqlalchemy import func

from database import session
from db_models.anime import Anime
from db_models.seasons import Seasons
from enums.db_enums import ReviewStatus

# 21 days is 3 weeks (between 2 and 4 weeks)
DEFAULT_QUARANTINE_DAYS = 21
DAYS_BEFORE_AIR_DATE = 7


def parse_date(date_str: str | None) -> date | None:
  """Parse various date string formats into a datetime.date object."""
  if not date_str:
    return None
  cleaned = str(date_str).strip().split('T')[0]
  for fmt in ('%Y-%m-%d', '%Y-%m', '%Y'):
    try:
      return datetime.strptime(cleaned, fmt).date()
    except ValueError:
      continue
  return None


def is_season_in_quarantine(
    season: Seasons,
    as_of_date: date | None = None,
    quarantine_days: int = DEFAULT_QUARANTINE_DAYS,
    days_before: int = DAYS_BEFORE_AIR_DATE,
) -> bool:
  """Check if a specific season is currently within the quarantine/embargo window.

  Quarantine starts `days_before` prior to the air date (e.g. 7 days before)
  and lasts until `quarantine_days` after the premiere (e.g. 21 days).
  """
  if not season or not season.air_date:
    return False

  air_d = parse_date(season.air_date)
  if not air_d:
    return False

  target_date = as_of_date or datetime.now(timezone.utc).date()
  quarantine_start = air_d - timedelta(days=days_before)
  quarantine_end = air_d + timedelta(days=quarantine_days)

  return quarantine_start <= target_date < quarantine_end


def get_latest_season(anime_id: int) -> Seasons | None:
  """Find the most recently aired or upcoming season for an anime."""
  seasons = session.query(Seasons).filter(Seasons.anime_id == anime_id).all()
  if not seasons:
    return None

  def sort_key(s: Seasons):
    d = parse_date(s.air_date)
    # Put dated seasons first, then sort by season_number and part
    return (d or date.min, s.season_number or 0, s.part or 0)

  return max(seasons, key=sort_key)


def check_and_update_quarantine_status(
    anime_id: int | None = None,
    as_of_date: date | None = None,
    quarantine_days: int = DEFAULT_QUARANTINE_DAYS,
    days_before: int = DAYS_BEFORE_AIR_DATE,
) -> dict:
  """Scan anime records and transition their ReviewStatus into or out of quarantine.

  - Moves to ReviewStatus.quarantine if any newly aired/upcoming season is in
  the window.
  - Moves to ReviewStatus.confirmed if the quarantine period has passed.

  Returns a dict with 'quarantined' and 'released' lists of anime IDs.
  """
  target_date = as_of_date or datetime.now(timezone.utc).date()

  query = session.query(Anime)
  if anime_id is not None:
    query = query.filter(Anime.id == anime_id)

  anime_list = query.all()
  quarantined_ids = []
  released_ids = []

  # Import inside function to avoid circular dependency
  from common_funcs.ratings import recalculate_anime_rating

  for anime in anime_list:
    seasons = session.query(Seasons).filter(Seasons.anime_id == anime.id).all()
    any_quarantined = any(
        is_season_in_quarantine(
            s,
            as_of_date=target_date,
            quarantine_days=quarantine_days,
            days_before=days_before,
        )
        for s in seasons
    )

    current_status = anime.status
    if hasattr(current_status, 'value'):
      current_status_val = current_status.value
    else:
      current_status_val = str(current_status)

    if any_quarantined:
      if current_status_val != ReviewStatus.quarantine.value:
        anime.status = ReviewStatus.quarantine
        quarantined_ids.append(anime.id)
    else:
      if current_status_val == ReviewStatus.quarantine.value:
        anime.status = ReviewStatus.confirmed
        released_ids.append(anime.id)
        # Recalculate aggregate ratings now that quarantine has expired
        recalculate_anime_rating(anime.id)

  session.commit()
  return {'quarantined': quarantined_ids, 'released': released_ids}
