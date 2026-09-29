import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from common_funcs.quarantine import check_and_update_quarantine_status
from common_funcs.ratings import submit_user_rating
from database import session
from db_models.anime import Anime
from db_models.ratings import Rating
from db_models.seasons import Seasons
from db_models.users import User
from enums.db_enums import AnimeType, ReviewStatus, SeasonType


def run_simulation():
  print("=" * 60)
  print("STEP 1: Create 'Foobar no Anime' that airs TODAY")
  print("=" * 60)

  title = "Foobar no Anime"
  # Cleanup if previously created
  existing = session.query(Anime).filter(Anime.title == title).all()
  for a in existing:
    session.query(Rating).filter(Rating.anime_id == a.id).delete()
    session.query(Seasons).filter(Seasons.anime_id == a.id).delete()
    session.delete(a)
  session.commit()

  today = datetime.now(timezone.utc).date()
  foobar = Anime(
      title=title,
      _type=AnimeType.show,
      status=ReviewStatus.confirmed,
      desc="A newly aired anime premiering today!",
      content_rating="PG-13",
  )
  session.add(foobar)
  session.commit()

  season = Seasons(
      season_number=1,
      anime_id=foobar.id,
      episodes=12,
      title="Foobar no Anime Season 1",
      air_date=today.isoformat(),
      type_season=SeasonType.SEASON,
  )
  session.add(season)
  session.commit()
  print(f"Created: {foobar.title} (ID: {foobar.id}), Air Date: {season.air_date}")

  print("\n" + "=" * 60)
  print("STEP 2: Run Cron Job / Quarantine Check")
  print("=" * 60)
  res = check_and_update_quarantine_status(anime_id=foobar.id)
  session.refresh(foobar)
  print(f"Quarantine Scan Result: {res}")
  print(f"Current ReviewStatus: {foobar.status}")

  print("\n" + "=" * 60)
  print("STEP 3: Simulate 5 Fake Users Submitting Hyped Ratings")
  print("=" * 60)
  user_scores = [10, 9, 10, 8, 10]
  for i, score in enumerate(user_scores, start=1):
    uname = f"sim_user_{i}"
    user = session.query(User).filter(User.username == uname).first()
    if not user:
      user = User(f"{uname}@example.com", "fakehash", uname)
      session.add(user)
      session.commit()
    submit_user_rating(user.id, foobar.id, score, season_id=season.id)
    print(f"User {uname} rated: {score}/10")

  session.refresh(foobar)
  json_output = foobar.make_json()
  print(f"\n[Verification] Anime DB Rating: {foobar.rating}")
  print(f"[Verification] Anime JSON Rating: {json_output['rating']}")
  print(f"[Verification] Quarantined Flag: {json_output['quarantined']}")
  if json_output['rating'] is None and json_output['quarantined'] is True:
    print(">>> SUCCESS: Ratings are SUPPRESSED and not shown during quarantine!")

  print("\n" + "=" * 60)
  print("STEP 4: Fast Forward Air Date to 4 Weeks Ago (28 days)")
  print("=" * 60)
  past_date = today - timedelta(days=28)
  season.air_date = past_date.isoformat()
  session.commit()
  print(f"Updated Season Air Date to: {season.air_date}")

  print("\n" + "=" * 60)
  print("STEP 5: Run Quarantine Check Cron Job Again")
  print("=" * 60)
  res = check_and_update_quarantine_status(anime_id=foobar.id)
  session.refresh(foobar)
  print(f"Quarantine Scan Result: {res}")
  print(f"Current ReviewStatus: {foobar.status}")

  json_output = foobar.make_json()
  print(f"\n[Verification] Anime DB Rating: {foobar.rating}")
  print(f"[Verification] Anime JSON Rating: {json_output['rating']}")
  print(f"[Verification] Quarantined Flag: {json_output['quarantined']}")
  expected_avg = round(sum(user_scores) / len(user_scores), 2)
  if json_output['rating'] == expected_avg and json_output['quarantined'] is False:
    print(f">>> SUCCESS: Embargo lifted! Ratings now aggregated and displayed: {json_output['rating']}/10")


if __name__ == "__main__":
  run_simulation()
