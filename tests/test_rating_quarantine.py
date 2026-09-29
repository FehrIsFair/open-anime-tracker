from datetime import date, datetime, timedelta, timezone

import pytest

from common_funcs.quarantine import check_and_update_quarantine_status
from common_funcs.ratings import (
    calculate_aggregated_rating,
    recalculate_anime_rating,
    submit_user_rating,
)
from database import session
from db_models.anime import Anime
from db_models.ratings import Rating
from db_models.seasons import Seasons
from db_models.users import User
from enums.db_enums import AnimeType, ReviewStatus, SeasonType
from main import app


@pytest.fixture(scope="module")
def client():
  app.config["TESTING"] = True
  with app.test_client() as test_client:
    yield test_client


@pytest.fixture
def fake_users():
  """Create 5 fake users for testing ratings."""
  users = []
  for i in range(1, 6):
    uname = f"test_sim_user_{i}"
    user = session.query(User).filter(User.username == uname).first()
    if not user:
      user = User(f"{uname}@example.com", "fakehash", uname)
      session.add(user)
  session.commit()

  for i in range(1, 6):
    u = session.query(User).filter(User.username == f"test_sim_user_{i}").first()
    users.append(u)
  return users


def cleanup_anime_by_title(title: str):
  existing = session.query(Anime).filter(Anime.title == title).all()
  for a in existing:
    session.query(Rating).filter(Rating.anime_id == a.id).delete()
    session.query(Seasons).filter(Seasons.anime_id == a.id).delete()
    session.delete(a)
  session.commit()


def test_foobar_quarantine_simulation(client, fake_users):
  title = "Foobar no Anime"
  cleanup_anime_by_title(title)

  today_str = datetime.now(timezone.utc).date().isoformat()

  # 1. Create 'Foobar no Anime' that airs today
  foobar = Anime(
      title=title,
      _type=AnimeType.show,
      status=ReviewStatus.confirmed,
      desc="A test anime currently airing today.",
      content_rating="PG-13",
  )
  session.add(foobar)
  session.commit()

  season1 = Seasons(
      season_number=1,
      anime_id=foobar.id,
      episodes=12,
      title="Foobar no Anime Season 1",
      air_date=today_str,
      type_season=SeasonType.SEASON,
  )
  session.add(season1)
  session.commit()

  # 2. Run quarantine check (cron job simulation)
  check_result = check_and_update_quarantine_status(anime_id=foobar.id)
  session.refresh(foobar)

  assert foobar.id in check_result["quarantined"]
  assert foobar.status == ReviewStatus.quarantine

  # 3. Simulate multiple users rating Foobar no Anime
  ratings_to_give = [9, 10, 8, 9, 10]  # Average = 9.2
  for user, score in zip(fake_users, ratings_to_give):
    submit_user_rating(
        user_id=user.id,
        anime_id=foobar.id,
        rating_value=score,
        season_id=season1.id,
    )

  session.refresh(foobar)

  # 4. Ratings must NOT show up while quarantined
  assert foobar.rating is None
  json_data = foobar.make_json()
  assert json_data["rating"] is None
  assert json_data["quarantined"] is True

  # Check endpoint response
  res = client.get(f"/anime/{foobar.id}")
  assert res.status_code == 200
  body = res.get_json()
  assert body["anime"]["rating"] is None
  assert body["anime"]["quarantined"] is True
  assert body["seasons"][0]["rating"] is None
  assert body["seasons"][0]["quarantined"] is True

  # 5. Move air date to 4 weeks (28 days) in the past
  past_date = (datetime.now(timezone.utc).date() - timedelta(days=28)).isoformat()
  season1.air_date = past_date
  session.commit()

  # 6. Run un-quarantine check (cron job simulation)
  check_result = check_and_update_quarantine_status(anime_id=foobar.id)
  session.refresh(foobar)

  assert foobar.id in check_result["released"]
  assert foobar.status == ReviewStatus.confirmed

  # 7. Ratings MUST now show up and be aggregated
  assert foobar.rating == 9.2
  json_data = foobar.make_json()
  assert json_data["rating"] == 9.2
  assert json_data["quarantined"] is False

  # Check endpoint response
  res = client.get(f"/anime/{foobar.id}")
  assert res.status_code == 200
  body = res.get_json()
  assert body["anime"]["rating"] == 9.2
  assert body["anime"]["quarantined"] is False
  assert body["seasons"][0]["rating"] == 9.2
  assert body["seasons"][0]["quarantined"] is False

  # Clean up test anime
  cleanup_anime_by_title(title)


def test_multi_season_quarantine_latest_season(client, fake_users):
  """Verify that a multi-season show is quarantined if its newest season is airing."""
  title = "MultiSeason Test Show"
  cleanup_anime_by_title(title)

  today_str = datetime.now(timezone.utc).date().isoformat()
  old_air_date = (datetime.now(timezone.utc).date() - timedelta(days=365)).isoformat()

  anime = Anime(
      title=title,
      _type=AnimeType.show,
      status=ReviewStatus.confirmed,
      desc="Multi-season show with an airing latest season.",
      content_rating="PG-13",
  )
  session.add(anime)
  session.commit()

  # Season 1 aired a year ago
  s1 = Seasons(
      season_number=1,
      anime_id=anime.id,
      episodes=12,
      title="Season 1",
      air_date=old_air_date,
      type_season=SeasonType.SEASON,
  )
  # Season 2 airs today
  s2 = Seasons(
      season_number=2,
      anime_id=anime.id,
      episodes=12,
      title="Season 2",
      air_date=today_str,
      type_season=SeasonType.SEASON,
  )
  session.add_all([s1, s2])
  session.commit()

  # Rate Season 1
  for user in fake_users[:3]:
    submit_user_rating(user.id, anime.id, 8, season_id=s1.id)

  # Run quarantine check -> anime should be quarantined because Season 2 is airing
  res = check_and_update_quarantine_status(anime_id=anime.id)
  session.refresh(anime)

  assert anime.id in res["quarantined"]
  assert anime.status == ReviewStatus.quarantine
  assert anime.make_json()["rating"] is None

  # Rate Season 2 with hyped 10s
  for user in fake_users:
    submit_user_rating(user.id, anime.id, 10, season_id=s2.id)

  # Check endpoint: Season 2 rating is hidden, overall anime rating is hidden
  res = client.get(f"/anime/{anime.id}")
  body = res.get_json()
  assert body["anime"]["rating"] is None
  assert body["anime"]["quarantined"] is True

  # Advance Season 2 air date 30 days in the past
  s2.air_date = (datetime.now(timezone.utc).date() - timedelta(days=30)).isoformat()
  session.commit()

  # Run quarantine check again -> unquarantined
  res = check_and_update_quarantine_status(anime_id=anime.id)
  session.refresh(anime)

  assert anime.id in res["released"]
  assert anime.status == ReviewStatus.confirmed
  # Ratings are now visible and aggregated
  assert anime.rating is not None
  assert anime.make_json()["quarantined"] is False

  cleanup_anime_by_title(title)
