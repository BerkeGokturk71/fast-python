from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import setting
engine = create_engine(setting.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
