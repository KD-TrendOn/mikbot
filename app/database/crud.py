from sqlalchemy.orm import Session
from . import models
from ..schemas.state import State, SubState
from ..services.vector_store import get_vectorstore

async def load_service_data(db: Session, service_name: str):
    return db.query(models.Service).filter(models.Service.name == service_name).first()

async def load_tools(db: Session, service_name: str):
    service = await load_service_data(db, service_name)
    return db.query(models.Tool).filter(models.Tool.service_id == service.id).all()

async def load_vector_documents(service_name: str, query: str, k: int = 5):
    vectorstore = get_vectorstore()
    docs = await vectorstore.asimilarity_search_with_score(query, k=k, filter={"service": service_name})
    return docs
