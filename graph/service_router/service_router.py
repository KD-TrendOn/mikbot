from langchain.output_parsers import PydanticOutputParser
from ..schemas import RouterAnswer, State
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from .model_init import init_chat_model

parser = PydanticOutputParser(pydantic_object=RouterAnswer)
format_instructions = parser.get_format_instructions()
async def service_router(state: State, config: RunnableConfig) -> State:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a service router. Determine which service the user's request is related to: 'accounts', 'cards', or 'parking'. Use next scheme for answer: {formatted_instructions}"),
        ("human", "{user_input}")
    ])
    chain = prompt | init_chat_model(mode="light") | parser
    service = await chain.ainvoke({"user_input": state["user_input"], "formatted_instructions":format_instructions})
    return {"service": service.answer}