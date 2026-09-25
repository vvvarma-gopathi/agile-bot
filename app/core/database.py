from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from core.config import settings

engine=create_engine(settings.DATABASE_URL)
Base=declarative_base()
SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()