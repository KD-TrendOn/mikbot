from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, index=True)
    sender_role = Column(String)
    content = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    prompt = Column(Text)
    documentation = Column(Text)

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    function = Column(Text)
    input_schema = Column(Text)  # Добавляем это поле
    service_id = Column(Integer, ForeignKey("services.id"))
