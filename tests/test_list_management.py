from datetime import UTC, datetime
import pytest

from common_funcs.ratings import submit_user_rating
from database import session
from db_models.anime import Anime
from db_models.list import List
from db_models.ratings import Rating
from db_models.users import User
from enums.db_enums import AnimeType, ListStatus, ReviewStatus
from main import app
from project_exceptions.exceptions import InvalidEnumException
from routes.list import get_list_status


@pytest.fixture(scope="module")
def client():
  app.config["TESTING"] = True
  with app.test_client() as test_client:
    yield test_client


@pytest.fixture
def test_user():
  uname = "test_list_user_1"
  user = session.query(User).filter(User.username == uname).first()
  if not user:
    user = User(f"{uname}@example.com", "fakehash", uname)
    session.add(user)
    session.commit()
  return user


@pytest.fixture
def test_anime():
  title = "List Test Anime Unique"
  anime = session.query(Anime).filter(Anime.title == title).first()
  if not anime:
    anime = Anime(
        title=title,
        _type=AnimeType.show,
        status=ReviewStatus.confirmed,
        desc="A test anime for list management",
        content_rating="PG-13",
    )
    session.add(anime)
    session.commit()
  yield anime
  # Cleanup
  session.query(List).filter(List.anime_id == anime.id).delete()
  session.query(Rating).filter(Rating.anime_id == anime.id).delete()
  session.delete(anime)
  session.commit()


def test_list_status_enum_and_helper():
  assert ListStatus.plan_to_watch.value == 'plan_to_watch'
  assert ListStatus.watching.value == 'watching'
  assert ListStatus.complete.value == 'complete'
  assert ListStatus.dropped.value == 'dropped'
  assert ListStatus.on_hold.value == 'on_hold'

  assert get_list_status('plan_to_watch') == ListStatus.plan_to_watch
  assert get_list_status('watching') == ListStatus.watching
  assert get_list_status('complete') == ListStatus.complete
  assert get_list_status('dropped') == ListStatus.dropped
  assert get_list_status('on_hold') == ListStatus.on_hold

  with pytest.raises(InvalidEnumException):
    get_list_status('invalid_status_xyz')


def test_list_model_creation_and_make_json(test_user, test_anime):
  # Cleanup any existing
  session.query(List).filter(
      List.user_id == test_user.id, List.anime_id == test_anime.id
  ).delete()
  session.commit()

  item = List(
      anime_id=test_anime.id,
      user_id=test_user.id,
      status=ListStatus.watching,
  )
  session.add(item)
  session.commit()

  json_data = item.make_json()
  assert json_data['anime_id'] == test_anime.id
  assert json_data['user_id'] == test_user.id
  assert json_data['status'] == 'watching'
  assert json_data['created_at'] is not None
  assert json_data['updated_at'] is not None

  session.delete(item)
  session.commit()


def test_unauthenticated_requests(client, test_anime):
  # Clear session
  with client.session_transaction() as sess:
    sess.clear()

  res = client.get('/list')
  assert res.status_code == 401

  res = client.post('/list', json={'anime_id': test_anime.id})
  assert res.status_code == 401

  res = client.patch(f'/list/{test_anime.id}', json={'status': 'watching'})
  assert res.status_code == 401

  res = client.delete(f'/list/{test_anime.id}')
  assert res.status_code == 401


def test_authenticated_list_crud_flow(client, test_user, test_anime):
  with client.session_transaction() as sess:
    sess['username'] = test_user.username

  # 1. Add anime to list (default status: plan_to_watch)
  res = client.post('/list', json={'anime_id': test_anime.id})
  assert res.status_code == 200
  data = res.get_json()['data']
  assert data['status'] == 'plan_to_watch'
  assert data['anime_id'] == test_anime.id

  # 2. Check anime status endpoint
  res = client.get(f'/list/anime/{test_anime.id}')
  assert res.status_code == 200
  status_info = res.get_json()
  assert status_info['in_list'] is True
  assert status_info['status'] == 'plan_to_watch'

  # 3. Add personal rating
  submit_user_rating(
      user_id=test_user.id,
      anime_id=test_anime.id,
      rating_value=9,
      comment="Great test show!",
  )

  # 4. GET /list verifies joined anime and personal rating
  res = client.get('/list')
  assert res.status_code == 200
  list_items = res.get_json()['data']
  matched = [i for i in list_items if i['anime_id'] == test_anime.id]
  assert len(matched) == 1
  item = matched[0]
  assert item['status'] == 'plan_to_watch'
  assert item['anime']['title'] == test_anime.title
  assert item['user_rating'] is not None
  assert item['user_rating']['rating'] == 9
  assert item['user_rating']['comment'] == "Great test show!"

  # 5. Filter by status
  res = client.get('/list?status=watching')
  assert res.status_code == 200
  assert not any(i['anime_id'] == test_anime.id for i in res.get_json()['data'])

  res = client.get('/list?status=plan_to_watch')
  assert res.status_code == 200
  assert any(i['anime_id'] == test_anime.id for i in res.get_json()['data'])

  # 6. PATCH /list/<anime_id> to 'watching'
  res = client.patch(f'/list/{test_anime.id}', json={'status': 'watching'})
  assert res.status_code == 200
  assert res.get_json()['data']['status'] == 'watching'

  # 7. POST /list upsert: change to 'complete'
  res = client.post(
      '/list', json={'anime_id': test_anime.id, 'status': 'complete'}
  )
  assert res.status_code == 200
  assert res.get_json()['data']['status'] == 'complete'

  # 8. DELETE /list/<anime_id>
  res = client.delete(f'/list/{test_anime.id}')
  assert res.status_code == 200

  # Verify removed
  res = client.get(f'/list/anime/{test_anime.id}')
  assert res.status_code == 200
  assert res.get_json()['in_list'] is False
