import datetime

from sqlalchemy import TIMESTAMP, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    type_annotation_map = {  # noqa: RUF012
        datetime.datetime: TIMESTAMP(timezone=True)
    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()