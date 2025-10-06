from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
from collections.abc import Generator

load_dotenv()
Db_url = os.getenv("DATABASE_URL")
engine = create_engine(Db_url)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session"""
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
