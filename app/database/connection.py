from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from ..config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Добавьте Vector в модели, где это необходимо
# Например, в VectorDocument:
# embedding = Column(Vector(1536))  # Размерность вектора зависит от используемой модели эмбеддингов
