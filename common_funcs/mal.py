from requests import request

from const import mal_api_base
from const import mal_client_secret
from database import session
from db_models.anime import Anime
from db_models.seasons import Seasons
from enums.db_enums import AnimeType, ReviewStatus, SeasonType


class MALClient:
    pass
