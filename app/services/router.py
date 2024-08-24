from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from ..schemas.state import State, create_router_answer
from .llm import init_chat_model
from ..database.crud import get_all_services
from langchain.pydantic_v1 import BaseModel, Field
from typing import Literal
router_parser = None

async def update_router_parser(db):
    global router_parser
    services = await get_all_services(db)
    service_names = [service.name for service in services]
    RouterAnswer = create_router_answer(service_names)
    router_parser = PydanticOutputParser(pydantic_object=RouterAnswer)

class DullRouterAnswer(BaseModel):
    answer:Literal["Финансовый аналитик", "Бот навигатор по приложению"] = Field(description="Указывает на название выбранного для ответа сервиса. 'Финансовый аналитик' либо 'Бот навигатор по приложению'")


dull_router_parser = PydanticOutputParser(pydantic_object=DullRouterAnswer)
async def service_router(state: State, config: RunnableConfig) -> State:
    db = state.metadata.get("db")
    if db is None:
        raise ValueError("Database session is not available")

    if router_parser is None:
        await update_router_parser(db)

    # Получаем все сервисы из базы данных
    services = await get_all_services(db)
    
    # Создаем строку с описанием всех сервисов
    services_description = "\n".join([f"- {service.name}: {service.documentation}" for service in services])
    
    # Создаем список названий сервисов для использования в инструкциях формата
    service_names = [service.name for service in services]

    prompt_template = """You are a service router for the Tatarstan Resident Card application. 
    Determine which service the user's request is related to from the following list of available services:
    {services_description}

    Use the following format for your answer: {format_instructions}

    Chat history:
    {chat_history}

    Current user's input: {user_input}

    Based on the chat history, the current user's input, and the available services, determine the most appropriate service.
    If this is the first message in the conversation, or if the topic has clearly changed, choose the service that best matches the current input.
    If the conversation is continuing on the same topic, prefer to use the same service as the last message unless the topic has clearly changed.
    """
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["services_description", "chat_history", "user_input"],
        partial_variables={"format_instructions": dull_router_parser.get_format_instructions()}
    )
    
    llm = init_chat_model(mode="light")
    chain = prompt | llm | dull_router_parser
    
    # Подготовим историю чата для промпта
    chat_history = ""
    for message in state.chat_history[-5:]:  # Берем последние 5 сообщений
        role = "User" if message.sender_role == "user" else "Assistant"
        content = message.content.get('message', '')
        service = message.content.get('service', '')
        chat_history += f"{role}: {content}\n"
        if service:
            chat_history += f"(Service used: {service})\n"
    
    result = await chain.ainvoke({
        "services_description": services_description,
        "chat_history": chat_history,
        "user_input": state.user_input
    })
    
    # Проверяем, что выбранный сервис существует
    if result.answer not in service_names:
        raise ValueError(f"Selected service '{result.answer}' is not in the list of available services")

    # Обновляем существующее состояние
    state_dict = state.dict()
    state_dict['service'] = result.answer
    return state_dict
