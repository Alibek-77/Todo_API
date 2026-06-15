from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlalchemy import create_engine
from settings import Settings
settings=Settings()
DATABASE_URL=settings.database_url
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
class Base(DeclarativeBase):
    pass
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()