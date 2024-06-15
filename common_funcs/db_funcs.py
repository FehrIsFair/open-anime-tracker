from database import session
from db_models.base import Base


def get_first(json_compare, compare_key, model: 'Base') -> 'Base':
  """
    This function returns the first item given the compared value and model.
    :param json_compare: Can be any type that can be stored in the database.
    :param compare_key: This is the attribute of the model that we want to compare.
    :param model: This is the model we want to use.
  """
  item = session.query(model).filter(model.__getattribute__(compare_key) == json_compare).first()
  return item
