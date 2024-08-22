from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from ..schemas.state import State, RouterOutput
from .llm import init_chat_model

router_parser = PydanticOutputParser(pydantic_object=RouterOutput)

async def service_router(state: State, config: RunnableConfig) -> State:
    prompt_template = """You are a service router for the Tatarstan Resident Card application. 
    Determine which service the user's request is related to: 'accounts' or 'parking'. 
    Use the following format for your answer: {format_instructions}

    Chat history:
    {chat_history}

    Current user's input: {user_input}

    Based on the chat history and the current user's input, determine the most appropriate service.
    If this is the first message in the conversation, or if the topic has clearly changed, choose the service that best matches the current input.
    If the conversation is continuing on the same topic, prefer to use the same service as the last message unless the topic has clearly changed.
    """
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["chat_history", "user_input"],
        partial_variables={"format_instructions": router_parser.get_format_instructions()}
    )
    
    llm = init_chat_model(mode="light")
    chain = prompt | llm | router_parser
    
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
        "chat_history": chat_history,
        "user_input": state.user_input
    })
    
    # Обновляем существующее состояние
    state_dict = state.dict()
    state_dict['service'] = result.service
    return state_dict
