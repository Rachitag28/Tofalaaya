import os
import logging
import functools
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import base_model

logger = logging.getLogger(__name__)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost/tofalaaya"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
    future=True
)


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


def init_db():
    base_model.Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def managed_transaction(func):
    """
    Handles commit / rollback automatically.
    Should be used ONLY in service layer functions.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        db: Session | None = kwargs.get("db")

        # If db is not provided, create one
        created_locally = False
        if db is None:
            db = SessionLocal()
            kwargs["db"] = db
            created_locally = True

        try:
            result = func(*args, **kwargs)
            db.commit()
            return result
        except Exception:
            db.rollback()
            logger.exception("Transaction rolled back")
            raise
        finally:
            if created_locally:
                db.close()

    return wrapper
