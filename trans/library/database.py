from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
)

Base = declarative_base()


def get_session(connection_string):
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return scoped_session(Session)
