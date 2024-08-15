from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from typing import TypedDict, List, Literal, Dict
from .schemas import State
from .graph import graph_runtime
async def process_user_input(user_input: str, user_id: str) -> Dict[str, str]:
    initial_state = {'messages':[('user', user_input)], "user_input":user_input, 'user_id':user_id}
    
    
    config = RunnableConfig(
        configurable={
            "user_id": user_id,
        }
    )
    
    
    result = await graph_runtime.ainvoke(initial_state, config=config)
    return {
        "answer": result['answer'],
        "messages":result["messages"]
    }
