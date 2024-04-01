from sqlalchemy.orm import DeclarativeBase
import sqlalchemy.ext.declarative as dec


class Base(DeclarativeBase):

  def make_json(self):
    """
      You need to override this function to manipulate the data inside this object, so you can get yourself a JSON
      friendly dict for returning a response.
    """


SqlAlchemyBase = dec.declarative_base()
