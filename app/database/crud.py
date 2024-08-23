from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models
from ..schemas.state import State, SubState
from ..tools.wrapper import ToolWrapper
import dill
from typing import List, Callable, Optional
from ..services.vector_store import get_vectorstore
from typing import List, Dict, Any
from datetime import datetime

def serialize_function(func: Callable) -> str:
    return dill.dumps(func).hex()

def deserialize_function(serialized_func: str) -> Callable:
    return dill.loads(bytes.fromhex(serialized_func))

async def load_service_data(db: AsyncSession, service_name: str) -> Optional[models.Service]:
    stmt = select(models.Service).where(models.Service.name == service_name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def load_tools(db: AsyncSession, service_name: str) -> List[ToolWrapper]:
    service = await load_service_data(db, service_name)
    if not service:
        return []
    
    stmt = select(models.Tool).where(models.Tool.service_id == service.id)
    result = await db.execute(stmt)
    tools = result.scalars().all()
    
    return [ToolWrapper(
        name=tool.name,
        description=tool.description,
        function=deserialize_function(tool.function),
        input_schema=deserialize_function(tool.input_schema)
    ) for tool in tools if tool.function and tool.input_schema]

async def save_tool(db: AsyncSession, tool: ToolWrapper, service_id: int) -> models.Tool:
    db_tool = models.Tool(
        name=tool.name,
        description=tool.description,
        function=serialize_function(tool.function),
        input_schema=serialize_function(tool.input_schema),
        service_id=service_id
    )
    db.add(db_tool)
    await db.commit()
    await db.refresh(db_tool)
    return db_tool

async def save_service(db: AsyncSession, service_name: str, prompt: str, documentation: str) -> models.Service:
    db_service = models.Service(
        name=service_name,
        prompt=prompt,
        documentation=documentation
    )
    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)
    return db_service

async def get_or_create_service(db: AsyncSession, service_name: str, prompt: str = "", documentation: str = "") -> models.Service:
    service = await load_service_data(db, service_name)
    if not service:
        service = await save_service(db, service_name, prompt, documentation)
    return service

async def update_service(db: AsyncSession, service_id: int, prompt: str = None, documentation: str = None) -> Optional[models.Service]:
    stmt = select(models.Service).where(models.Service.id == service_id)
    result = await db.execute(stmt)
    service = result.scalar_one_or_none()
    
    if service:
        if prompt is not None:
            service.prompt = prompt
        if documentation is not None:
            service.documentation = documentation
        await db.commit()
        await db.refresh(service)
    
    return service

async def delete_tool(db: AsyncSession, tool_id: int) -> bool:
    stmt = select(models.Tool).where(models.Tool.id == tool_id)
    result = await db.execute(stmt)
    tool = result.scalar_one_or_none()
    
    if tool:
        await db.delete(tool)
        await db.commit()
        return True
    return False

async def update_tool(db: AsyncSession, tool_id: int, name: str = None, description: str = None, function: Callable = None) -> Optional[models.Tool]:
    stmt = select(models.Tool).where(models.Tool.id == tool_id)
    result = await db.execute(stmt)
    tool = result.scalar_one_or_none()
    
    if tool:
        if name is not None:
            tool.name = name
        if description is not None:
            tool.description = description
        if function is not None:
            tool.function = serialize_function(function)
        await db.commit()
        await db.refresh(tool)
    
    return tool

async def load_vector_documents(service_name: str, query: str, k: int = 5):
    vectorstore = get_vectorstore()
    docs = await vectorstore.asimilarity_search_with_score(query, k=k, filter={"service": service_name})
    return docs

async def create_chat_message(db: AsyncSession, user_id: str, sender_role: str, content: Dict[str, Any]) -> models.ChatMessage:
    db_message = models.ChatMessage(user_id=user_id, sender_role=sender_role, content=content)
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message

async def get_chat_history(db: AsyncSession, user_id: str, limit: int = 10) -> List[models.ChatMessage]:
    query = select(models.ChatMessage).where(models.ChatMessage.user_id == user_id).order_by(models.ChatMessage.timestamp.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_all_services(db: AsyncSession):
    stmt = select(models.Service)
    result = await db.execute(stmt)
    return result.scalars().all()
