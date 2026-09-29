import json
import os
import re
import sys
from pathlib import Path
from urllib.request import urlretrieve

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from database import session
from db_models.anime import Anime
from db_models.seasons import Seasons
from enums.db_enums import AnimeType, ReviewStatus, SeasonType

DATA_URL = "https://github.com/manami-project/anime-offline-database/releases/latest/download/anime-offline-database-minified.json"
DATA_FILE = ROOT_DIR / "data" / "anime-offline-database-minified.json"

ROMAN_MAP = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7}

SEASON_PATTERNS = [
    # E.g. Shingeki no Kyojin Season 3 Part 2
    (r"^(.*?)(?:\s*:)?\s+Season\s+(\d+)\s+Part\s+(\d+)", lambda m: (m.group(1), int(m.group(2)), int(m.group(3)))),
    # E.g. Attack on Titan: The Final Season Part 2
    (r"^(.*?)(?:\s*:)?\s+(?:The\s+)?Final\s+Season\s+Part\s+(\d+)", lambda m: (m.group(1), 4, int(m.group(2)))),
    # E.g. Attack on Titan: The Final Season
    (r"^(.*?)(?:\s*:)?\s+(?:The\s+)?Final\s+Season", lambda m: (m.group(1), 4, None)),
    # E.g. 2nd Season Part 2
    (r"^(.*?)(?:\s*:)?\s+(\d+)(?:st|nd|rd|th)\s+Season\s+Part\s+(\d+)", lambda m: (m.group(1), int(m.group(2)), int(m.group(3)))),
    # E.g. 2nd Season / 3rd Season / 4th Season
    (r"^(.*?)(?:\s*:)?\s+(\d+)(?:st|nd|rd|th)\s+Season", lambda m: (m.group(1), int(m.group(2)), None)),
    # E.g. Season 2 / Season 3
    (r"^(.*?)(?:\s*:)?\s+Season\s+(\d+)", lambda m: (m.group(1), int(m.group(2)), None)),
    # E.g. Mob Psycho 100 II / III
    (r"^(.*?)\s+(II|III|IV|V|VI|VII)$", lambda m: (m.group(1), ROMAN_MAP.get(m.group(2).upper(), 2), None)),
    # E.g. Code Geass R2
    (r"^(.*?)(?:\s*:)?\s+R2$", lambda m: (m.group(1), 2, None)),
    # E.g. Part 2 / Part 3
    (r"^(.*?)(?:\s*:)?\s+Part\s+(\d+)$", lambda m: (m.group(1), 1, int(m.group(2)))),
]


def parse_season_info(title: str):
    for pattern, extractor in SEASON_PATTERNS:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            base, season_num, part_num = extractor(match)
            return base.strip(" :-"), season_num, part_num
    return title.strip(), 1, None


def map_type(raw_type: str) -> tuple[AnimeType, SeasonType]:
    match (raw_type or "").upper():
        case "MOVIE":
            return AnimeType.movie, SeasonType.SPECIAL
        case "ONA":
            return AnimeType.show, SeasonType.ONA
        case "OVA":
            return AnimeType.show, SeasonType.OVA
        case _:
            return AnimeType.show, SeasonType.SEASON


def ensure_dataset() -> Path:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading dataset from {DATA_URL}...")
        urlretrieve(DATA_URL, DATA_FILE)
        print("Download complete.")
    return DATA_FILE


def collect_canonical_shows(target_count: int = 500):
    dataset_path = ensure_dataset()
    with open(dataset_path, encoding="utf-8") as f:
        data = json.load(f)

    # Filter out unreleased, recap, or untrusted entries
    candidates = [
        x for x in data.get("data", [])
        if x.get("status") in ("FINISHED", "ONGOING")
        and x.get("type") in ("TV", "MOVIE", "ONA", "OVA")
        and x.get("score") and x["score"].get("arithmeticMean")
        and len(x.get("sources", [])) >= 6
        and "hentai" not in x.get("tags", [])
        and "recap" not in x.get("tags", [])
        and "compilation" not in x.get("tags", [])
    ]

    # Rank by rating
    candidates.sort(key=lambda x: x["score"]["arithmeticMean"], reverse=True)

    shows: dict[str, dict] = {}
    for item in candidates:
        base_title, season_num, part_num = parse_season_info(item["title"])
        if base_title not in shows:
            if len(shows) >= target_count:
                continue
            shows[base_title] = {
                "base_title": base_title,
                "seasons": [],
                "primary_entry": item,
            }

        shows[base_title]["seasons"].append({
            "season_number": season_num,
            "part": part_num,
            "title": item["title"],
            "episodes": item.get("episodes"),
            "rating": round(item["score"]["arithmeticMean"], 2),
            "type": item.get("type"),
            "season_info": item.get("animeSeason"),
            "raw": item,
        })

    return shows


def seed_database(target_count: int = 500, dry_run: bool = False):
    shows = collect_canonical_shows(target_count)
    print(f"Found {len(shows)} canonical shows for seeding.")

    if dry_run:
        print("Dry run completed successfully.")
        return

    # Check for existing titles to avoid duplicate inserts
    existing_titles = set(r[0] for r in session.query(Anime.title).all())

    inserted_shows = 0
    inserted_seasons = 0

    for base_title, show_data in shows.items():
        if base_title in existing_titles:
            continue

        primary = show_data["primary_entry"]
        anime_type, _ = map_type(primary.get("type", "TV"))
        seasons_list = show_data["seasons"]

        # Sort seasons by season_number, then part
        seasons_list.sort(key=lambda s: (s["season_number"], s["part"] or 0))

        # Re-index season numbers sequentially if needed
        # (e.g. if S1, S3 were parsed, keep sequential 1..N while preserving part)
        total_episodes = sum(s["episodes"] or 0 for s in seasons_list) or None

        # Build clean description from tags and studios
        tags = primary.get("tags", [])[:5]
        studios = primary.get("studios", [])
        desc_parts = []
        if tags:
            desc_parts.append(f"Genres: {', '.join(tags).title()}")
        if studios:
            desc_parts.append(f"Studios: {', '.join(studios).title()}")
        desc = " | ".join(desc_parts) if desc_parts else None

        # Extract Japanese title from synonyms if present
        jp_title = None
        for syn in primary.get("synonyms", []):
            if re.search(r"[\u3040-\u30ff\u4e00-\u9faf]", syn):
                jp_title = syn
                break

        # Calculate average rating across seasons
        season_ratings = [s["rating"] for s in seasons_list if s.get("rating")]
        overall_rating = (
            round(sum(season_ratings) / len(season_ratings), 2)
            if season_ratings
            else round(primary["score"]["arithmeticMean"], 2)
        )

        metadata = {
            "picture": primary.get("picture"),
            "thumbnail": primary.get("thumbnail"),
            "sources": primary.get("sources", []),
            "synonyms": primary.get("synonyms", []),
            "studios": studios,
            "tags": primary.get("tags", []),
        }

        anime = Anime(
            title=base_title,
            _type=anime_type,
            status=ReviewStatus.confirmed,
            jp_title=jp_title,
            other_titles=metadata,
            rating=overall_rating,
            seasons=len(seasons_list),
            episodes=total_episodes,
            desc=desc,
            content_rating="PG-13",
        )
        session.add(anime)
        session.flush()  # populate anime.id

        # Insert seasons
        for idx, s in enumerate(seasons_list, start=1):
            _, s_type = map_type(s["type"])
            season_year = s.get("season_info", {}).get("year") if s.get("season_info") else None
            air_date = str(season_year) if season_year else None

            season_record = Seasons(
                season_number=s["season_number"] if s["season_number"] > 0 else idx,
                anime_id=anime.id,
                episodes=s["episodes"],
                title=s["title"],
                desc=desc,
                rating=s["rating"],
                type_season=s_type,
                part=s["part"],
                air_date=air_date,
            )
            session.add(season_record)
            inserted_seasons += 1

        inserted_shows += 1

    session.commit()
    print(f"Successfully seeded {inserted_shows} shows and {inserted_seasons} seasons!")


if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    count = 500
    for arg in sys.argv:
        if arg.startswith("--count="):
            count = int(arg.split("=")[1])
    seed_database(target_count=count, dry_run=is_dry)
