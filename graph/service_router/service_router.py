from langchain.output_parsers import PydanticOutputParser
from ..schemas import RouterAnswer, State
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import PromptTemplate
from .model_init import init_chat_model

parser = PydanticOutputParser(pydantic_object=RouterAnswer)
format_instructions = parser.get_format_instructions()
async def service_router(state: State, config: RunnableConfig) -> State:
    print("2")
    prompt_template = "You are a service router. Determine which service the user's request is related to: 'accounts', 'cards', or 'parking'. Use next scheme for answer: {formatted_instructions}. User's input: {user_input}"
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | init_chat_model(mode="light") | parser
    service = chain.invoke({"user_input": state["user_input"], "formatted_instructions":format_instructions})
    print(service.answer)
    return {"service": service.answer}