from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from ..schemas.state import State, RouterOutput
from .llm import init_chat_model

router_parser = PydanticOutputParser(pydantic_object=RouterOutput)

async def service_router(state: State, config: RunnableConfig) -> State:
    prompt_template = """You are a service router for the Tatarstan Resident Card application. 
    Determine which service the user's request is related to: 'accounts', 'cards', 'parking', or 'legal_assistant'. 
    Use the following format for your answer: {format_instructions}

    User's input: {user_input}
    """
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["user_input"],
        partial_variables={"format_instructions": router_parser.get_format_instructions()}
    )
    
    llm = init_chat_model(mode="light")
    chain = prompt | llm | router_parser
    
    result = await chain.ainvoke({"user_input": state.user_input})
    
    return State(**state.dict(), service=result.service)