from sqlalchemy.orm import DeclarativeBase
import sqlalchemy.ext.declarative as dec


class Base(DeclarativeBase):
  pass


SqlAlchemyBase = dec.declarative_base()
