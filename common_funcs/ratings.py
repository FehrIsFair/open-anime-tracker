from datetime import UTC, datetime
from sqlalchemy import func

from database import session
from db_models.anime import Anime
from db_models.ratings import Rating
from db_models.seasons import Seasons
from db_models.users import User
from enums.db_enums import ReviewStatus


def submit_user_rating(
    user_id: int,
    anime_id: int,
    rating_value: int,
    season_id: int | None = None,
    comment: str | None = None,
) -> Rating:
  """Submit or update a user rating for an anime show or specific season.

  Args:
    user_id: ID of the rating user.
    anime_id: ID of the parent anime.
    rating_value: Score between 1 and 10.
    season_id: Optional ID of the specific season being rated.
    comment: Optional brief commentary blurb (up to 500 characters).

  Returns:
    The created or updated Rating record.
  """
  if not isinstance(rating_value, int) or rating_value < 1 or rating_value > 10:
    raise ValueError('Rating must be an integer between 1 and 10')

  clean_comment = None
  if comment is not None:
    if not isinstance(comment, str):
      raise ValueError('Comment must be a string')
    clean_comment = comment.strip()
    if len(clean_comment) > 500:
      raise ValueError('Comment cannot exceed 500 characters')
    if not clean_comment:
      clean_comment = None

  anime = session.query(Anime).filter(Anime.id == anime_id).first()
  if not anime:
    raise ValueError(f'Anime with ID {anime_id} not found')

  if season_id is not None:
    season = (
        session.query(Seasons)
        .filter(Seasons.id == season_id, Seasons.anime_id == anime_id)
        .first()
    )
    if not season:
      raise ValueError(
          f'Season with ID {season_id} not found for Anime {anime_id}'
      )

  # Check for existing rating to perform an upsert
  existing = (
      session.query(Rating)
      .filter(
          Rating.user_id == user_id,
          Rating.anime_id == anime_id,
          Rating.season_id == season_id
          if season_id is not None
          else Rating.season_id.is_(None),
      )
      .first()
  )

  if existing:
    existing.rating = rating_value
    if comment is not None:
      existing.comment = clean_comment
    existing.updated_at = datetime.now(tz=UTC)
    rating_record = existing
  else:
    rating_record = Rating(
        user_id=user_id,
        rating=rating_value,
        anime_id=anime_id,
        season_id=season_id,
        comment=clean_comment,
    )
    session.add(rating_record)

  session.commit()

  # Update season rating if season_id was provided
  if season_id is not None:
    season_ratings = (
        session.query(func.avg(Rating.rating))
        .filter(Rating.season_id == season_id)
        .scalar()
    )
    if season_ratings is not None:
      season = session.query(Seasons).filter(Seasons.id == season_id).first()
      if season:
        season.rating = round(float(season_ratings), 2)
        session.commit()

  # Only recalculate and publish anime rating if NOT in quarantine
  anime_status = (
      anime.status.value if hasattr(anime.status, 'value') else anime.status
  )
  if anime_status != ReviewStatus.quarantine.value:
    recalculate_anime_rating(anime_id)

  return rating_record


def get_anime_reviews(
    anime_id: int,
    season_id: int | None = None,
    limit: int = 20,
) -> list[dict]:
  """Fetch recent ratings with blurbs/comments for an anime or specific season."""
  query = (
      session.query(Rating, User.username, Seasons.title)
      .join(User, Rating.user_id == User.id)
      .outerjoin(Seasons, Rating.season_id == Seasons.id)
      .filter(Rating.anime_id == anime_id)
  )

  if season_id is not None:
    query = query.filter(Rating.season_id == season_id)

  # Prioritize ratings that have non-null comments, then most recent
  results = (
      query.order_by(
          Rating.comment.is_(None),
          Rating.updated_at.desc(),
      )
      .limit(limit)
      .all()
  )

  reviews = []
  for r, username, season_title in results:
    reviews.append({
        'id': r.id,
        'user_id': r.user_id,
        'username': username,
        'rating': r.rating,
        'comment': r.comment,
        'anime_id': r.anime_id,
        'season_id': r.season_id,
        'season_title': season_title,
        'created_at': r.created_at.isoformat() if r.created_at else None,
        'updated_at': r.updated_at.isoformat() if r.updated_at else None,
    })
  return reviews



def calculate_aggregated_rating(anime_id: int) -> float | None:
  """Calculate the aggregated rating for an anime.

  Returns None if the anime is currently in ReviewStatus.quarantine.
  Combines direct show ratings and individual season ratings.
  """
  anime = session.query(Anime).filter(Anime.id == anime_id).first()
  if not anime:
    return None

  anime_status = (
      anime.status.value if hasattr(anime.status, 'value') else anime.status
  )
  # If currently quarantined, suppress aggregated rating
  if anime_status == ReviewStatus.quarantine.value:
    return None

  # Query user ratings for the show
  user_ratings = (
      session.query(Rating.rating).filter(Rating.anime_id == anime_id).all()
  )

  if user_ratings:
    scores = [r[0] for r in user_ratings]
    return round(sum(scores) / len(scores), 2)

  # Fallback to seeded season ratings if no user ratings exist yet
  season_ratings = (
      session.query(Seasons.rating)
      .filter(Seasons.anime_id == anime_id, Seasons.rating.is_not(None))
      .all()
  )

  if season_ratings:
    scores = [s[0] for s in season_ratings if s[0] is not None]
    if scores:
      return round(sum(scores) / len(scores), 2)

  return None


def recalculate_anime_rating(anime_id: int) -> float | None:
  """Recalculate and update the Anime.rating column in the database."""
  anime = session.query(Anime).filter(Anime.id == anime_id).first()
  if not anime:
    return None

  new_rating = calculate_aggregated_rating(anime_id)
  anime.rating = new_rating
  session.commit()
  return new_rating
