import datetime

from sqlalchemy import TIMESTAMP, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings

database_url = URL.create(
    drivername="postgresql",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=int(settings.database_port),
    database=settings.database_name,
)

SQLALCHEMY_DATABASE_URL = database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

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