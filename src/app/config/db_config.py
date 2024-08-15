from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.logger import my_logger
from app.core.settings import my_settings

SQLALCHEMY_DATABASE_URL = f"postgresql://admin:12345@postgres:5432/postgres"
db_engine = create_engine(SQLALCHEMY_DATABASE_URL)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
DBaseModel = declarative_base()


def init_db():
    db = db_session()
    print(f"init_db() : db = {type(db)}")
    try:
        yield db
    finally:
        db.close()
    print(f"init_db() : db.close()")
    return
