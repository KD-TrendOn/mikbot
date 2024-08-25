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
    answer:Literal["Анализ доходов и расходов и советы по финансовому плану", "Бот навигатор по приложению"] = Field(description="Указывает на название выбранного для ответа сервиса. 'Финансовый аналитик' либо 'Бот навигатор по приложению'")


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

    prompt_template = """Ты - умный маршрутизатор запросов в приложении "Карта жителя Республики Татарстан". Твоя задача - определить, какой сервис лучше всего подходит для обработки запроса пользователя.

Приложение "Карта жителя РТ" - это многофункциональное приложение, которое объединяет банковские и социальные сервисы. Пользователи обычно заходят в приложение, чтобы:
1. Проверить баланс и историю операций по карте
2. Совершить платежи (ЖКХ, детский сад, штрафы, налоги и т.д.)
3. Перевести деньги
4. Посмотреть доступные льготы и акции
5. Получить информацию о своих картах (банковской, транспортной, образовательной)
6. Проанализировать свои доходы и расходы
7. Получить помощь по использованию приложения

Доступные сервисы и их описания:
{services_description}

Внимательно проанализируй запрос пользователя и выбери наиболее подходящий сервис на основе их описаний.

История чата:
{chat_history}

Текущий запрос пользователя: {user_input}

На основе истории чата, текущего запроса пользователя и описания сервисов, определи наиболее подходящий сервис.
Если это первое сообщение в разговоре или если тема явно изменилась, выбери сервис, который лучше всего соответствует текущему запросу.
Если разговор продолжается на ту же тему, предпочти использовать тот же сервис, что и в последнем сообщении, если только тема явно не изменилась.

Используй следующий формат для своего ответа: {format_instructions}
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
