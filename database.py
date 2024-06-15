from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import const


engine = create_engine(f'postgresql://{const.PG_USER}:{const.PG_PW}@localhost:{const.PG_PORT}/db')

session = Session(engine)
