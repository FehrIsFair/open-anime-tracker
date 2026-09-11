from flask import Blueprint, make_response, request

from common_funcs.kitsu import (
  KitsuAPIError,
  KitsuDataError,
  fetch_and_store_kitsu_anime,
  import_seasons_to_anime,
)

kitsu_routes = Blueprint('kitsu', __name__)


@kitsu_routes.route('/anime/kitsu-import', methods=['POST'])
def kitsu_import():
  # Parse and validate request body
  try:
    body = request.get_json()
    if not body or 'kitsuId' not in body:
      return make_response({'message': 'Missing kitsuId in request body'}, 400)

    kitsu_id = body['kitsuId']
    if not isinstance(kitsu_id, int) or kitsu_id <= 0:
      return make_response({'message': 'kitsuId must be a positive integer'}, 400)
  except (ValueError, TypeError):
    return make_response({'message': 'Invalid request body'}, 400)

  # Call service layer
  try:
    result = fetch_and_store_kitsu_anime(kitsu_id)
    return make_response(result, 200)
  except (KitsuAPIError, KitsuDataError) as e:
    # 404 or malformed data from Kitsu
    return make_response({'message': str(e)}, 404)
  except ValueError as e:
    # Invalid input
    return make_response({'message': str(e)}, 400)
  except RuntimeError as e:
    # Database error
    return make_response({'message': str(e)}, 500)
  except Exception as e:  # noqa: BLE001
    # Unexpected error
    print(e)
    return make_response({'message': 'An unexpected error occurred'}, 500)


@kitsu_routes.route('/anime/kitsu-import-seasons', methods=['POST'])
def kitsu_import_seasons():
  # Parse and validate request body
  try:
    body = request.get_json()
    if not body or 'animeId' not in body:
      return make_response({'message': 'Missing animeId in request body'}, 400)

    anime_id = body['animeId']
    if not isinstance(anime_id, int) or anime_id <= 0:
      return make_response({'message': 'animeId must be a positive integer'}, 400)

    seasons = body.get('seasons')
    if not seasons or not isinstance(seasons, list) or len(seasons) == 0:
      return make_response({'message': 'At least one season is required'}, 400)

    for i, s in enumerate(seasons):
      sn = s.get('seasonNumber')
      kid = s.get('kitsuId')
      if not isinstance(sn, int) or sn <= 0:
        return make_response({'message': f'seasons[{i}].seasonNumber must be a positive integer'}, 400)
      if not isinstance(kid, int) or kid <= 0:
        return make_response({'message': f'seasons[{i}].kitsuId must be a positive integer'}, 400)
  except (ValueError, TypeError):
    return make_response({'message': 'Invalid request body'}, 400)

  # Call service layer
  try:
    result = import_seasons_to_anime(anime_id, seasons)
    return make_response(result, 200)
  except ValueError as e:
    return make_response({'message': str(e)}, 400)
  except RuntimeError as e:
    return make_response({'message': str(e)}, 500)
  except Exception as e:  # noqa: BLE001
    print(e)
    return make_response({'message': 'An unexpected error occurred'}, 500)
