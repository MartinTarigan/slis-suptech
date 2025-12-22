from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os

# DATABASE_URL dari .env
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set in .env!")

# Neon recommended: NullPool (avoid connection drop)
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=False,  # set True kalau mau lihat SQL logs
    future=True,
)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Base model untuk seluruh ORM
Base = declarative_base()

def get_db():
    """Dependency injection style (untuk Flask route)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
