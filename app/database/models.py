from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    prompt = Column(String)
    documentation = Column(String)

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    function = Column(String)  # Сериализованная функция
    service_id = Column(Integer, ForeignKey("services.id"))

# Удалим класс VectorDocument, так как теперь мы используем PGVector