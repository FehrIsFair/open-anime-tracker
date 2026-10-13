from datetime import UTC, datetime

from flask import Blueprint, make_response, request
from flask import session as sesh
from sqlalchemy import and_, func
from sqlalchemy.exc import SQLAlchemyError

from database import session
from db_models.anime import Anime
from db_models.list import List
from db_models.ratings import Rating
from db_models.users import User
from enums.db_enums import ListStatus
from project_exceptions.exceptions import InvalidEnumException

list_routes = Blueprint('list', __name__)


def get_list_status(status_str: str) -> ListStatus:
  """Validate and convert a string into a ListStatus enum."""
  for status in ListStatus:
    if status.value == status_str or status.name == status_str:
      return status
  raise InvalidEnumException(f'Value: {status_str} is not a valid List Status')


def get_current_user():
  """Helper to retrieve current authenticated user from session."""
  username = sesh.get('username')
  if not username:
    return None
  return session.query(User).filter(User.username == username).first()


@list_routes.route('/list', methods=['GET'])
def get_user_list():
  """Fetch authenticated user's anime list with metadata and personal ratings."""
  user = get_current_user()
  if not user:
    return make_response({'message': 'Authentication required'}, 401)

  status_filter = request.args.get('status')
  sort_param = request.args.get('sort', 'updated_desc')

  query = (
      session.query(List, Anime, Rating)
      .join(Anime, List.anime_id == Anime.id)
      .outerjoin(
          Rating,
          and_(
              Rating.user_id == user.id,
              Rating.anime_id == List.anime_id,
              Rating.season_id.is_(None),
          ),
      )
      .filter(List.user_id == user.id)
  )

  if status_filter:
    try:
      parsed_status = get_list_status(status_filter)
      query = query.filter(List.status == parsed_status)
    except InvalidEnumException:
      return make_response(
          {'message': f'Invalid status filter: {status_filter}'}, 400
      )

  # Apply sorting
  match sort_param:
    case 'rating_desc':
      query = query.order_by(Rating.rating.desc().nullslast(), Anime.title.asc())
    case 'rating_asc':
      query = query.order_by(Rating.rating.asc().nullslast(), Anime.title.asc())
    case 'title_asc':
      query = query.order_by(func.lower(Anime.title).asc())
    case 'title_desc':
      query = query.order_by(func.lower(Anime.title).desc())
    case _:  # default updated_desc
      query = query.order_by(List.updated_at.desc(), List.id.desc())

  try:
    results = query.all()
  except SQLAlchemyError as e:
    print(e)
    return make_response({'message': 'Failed to fetch list'}, 500)

  data = []
  for list_entry, anime, rating in results:
    item = list_entry.make_json()
    item['anime'] = anime.make_json()
    item['user_rating'] = rating.make_json() if rating else None
    data.append(item)

  return make_response({'data': data}, 200)


@list_routes.route('/list', methods=['POST'])
def add_to_list():
  """Add an anime to current user's list or update status if already present."""
  user = get_current_user()
  if not user:
    return make_response({'message': 'Authentication required'}, 401)

  body = request.get_json() or {}
  anime_id = body.get('anime_id')
  status_str = body.get('status', ListStatus.plan_to_watch.value)

  if not anime_id:
    return make_response({'message': 'Missing anime_id in request body'}, 400)

  try:
    status_enum = get_list_status(status_str)
  except InvalidEnumException:
    return make_response(
        {'message': f'Invalid status value: {status_str}'}, 400
    )

  anime = session.query(Anime).filter(Anime.id == anime_id).first()
  if not anime:
    return make_response({'message': 'Anime not found'}, 404)

  try:
    existing = (
        session.query(List)
        .filter(List.user_id == user.id, List.anime_id == anime_id)
        .first()
    )

    if existing:
      existing.status = status_enum
      existing.updated_at = datetime.now(tz=UTC)
      list_record = existing
    else:
      list_record = List(
          anime_id=anime_id,
          user_id=user.id,
          status=status_enum,
      )
      session.add(list_record)

    session.commit()
    return make_response(
        {
            'message': 'Anime saved to list',
            'data': list_record.make_json(),
        },
        200,
    )
  except SQLAlchemyError as e:
    print(e)
    session.rollback()
    return make_response({'message': 'Failed to save anime to list'}, 500)


@list_routes.route('/list/<int:anime_id>', methods=['PATCH'])
def update_list_status(anime_id):
  """Update watch status of an anime in current user's list."""
  user = get_current_user()
  if not user:
    return make_response({'message': 'Authentication required'}, 401)

  body = request.get_json() or {}
  status_str = body.get('status')
  if not status_str:
    return make_response({'message': 'Missing status in request body'}, 400)

  try:
    status_enum = get_list_status(status_str)
  except InvalidEnumException:
    return make_response(
        {'message': f'Invalid status value: {status_str}'}, 400
    )

  try:
    list_entry = (
        session.query(List)
        .filter(List.user_id == user.id, List.anime_id == anime_id)
        .first()
    )
    if not list_entry:
      return make_response({'message': 'Anime not in your list'}, 404)

    list_entry.status = status_enum
    list_entry.updated_at = datetime.now(tz=UTC)
    session.commit()

    return make_response(
        {
            'message': 'Status updated successfully',
            'data': list_entry.make_json(),
        },
        200,
    )
  except SQLAlchemyError as e:
    print(e)
    session.rollback()
    return make_response({'message': 'Failed to update list status'}, 500)


@list_routes.route('/list/<int:anime_id>', methods=['DELETE'])
def remove_from_list(anime_id):
  """Remove an anime from current user's list."""
  user = get_current_user()
  if not user:
    return make_response({'message': 'Authentication required'}, 401)

  try:
    list_entry = (
        session.query(List)
        .filter(List.user_id == user.id, List.anime_id == anime_id)
        .first()
    )
    if not list_entry:
      return make_response({'message': 'Anime not in your list'}, 404)

    session.delete(list_entry)
    session.commit()
    return make_response({'message': 'Anime removed from your list'}, 200)
  except SQLAlchemyError as e:
    print(e)
    session.rollback()
    return make_response({'message': 'Failed to remove anime from list'}, 500)


@list_routes.route('/list/anime/<int:anime_id>', methods=['GET'])
def get_anime_list_status(anime_id):
  """Check if an anime is in the authenticated user's list and return status."""
  user = get_current_user()
  if not user:
    return make_response({'message': 'Authentication required'}, 401)

  try:
    list_entry = (
        session.query(List)
        .filter(List.user_id == user.id, List.anime_id == anime_id)
        .first()
    )
    if list_entry:
      return make_response(
          {
              'in_list': True,
              'status': list_entry.status.value,
              'id': list_entry.id,
          },
          200,
      )
    return make_response({'in_list': False, 'status': None}, 200)
  except SQLAlchemyError as e:
    print(e)
    return make_response({'message': 'Failed to check anime list status'}, 500)
