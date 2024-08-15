from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from typing import TypedDict, List, Literal, Dict
from ..schemas import SubState
from .model_init import init_chat_model
# Создание подграфа для работника
def create_worker_subgraph(worker_name: str, worker_tools: List[tool]):
    
    
    async def load_service_docs(state: SubState, config: RunnableConfig) -> SubState:
        # Здесь должна быть логика загрузки документации для выбранного сервиса
        return {"useless":''}


    async def load_bot_docs(state: SubState, config: RunnableConfig) -> SubState:
        print(state)
        # Здесь должна быть логика загрузки документации бота
        return {"useless":''}


    async def process_message(state: SubState, config: RunnableConfig) -> SubState:
        print("1")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful banking assistant. Use the provided information to answer the user's question or call an appropriate tool."),
            ("human", "{user_input}")
        ])
        chain = prompt | init_chat_model(mode="main").bind_tools(tools=worker_tools)
        response = await chain.ainvoke({
            "user_input": state["user_input"],
        })
        return {"answer": response}


    subgraph = StateGraph(SubState)
    subgraph.add_node("load_service_docs", load_service_docs)
    subgraph.add_node("load_bot_docs", load_bot_docs)
    subgraph.add_node("process_message", process_message)
    subgraph.add_node("tools", ToolNode(worker_tools))


    subgraph.add_edge(START, "load_service_docs")
    subgraph.add_edge("load_service_docs", "load_bot_docs")
    subgraph.add_edge("load_bot_docs", "process_message")


    def should_continue(state: SubState) -> Literal["tools", "__end__"]:
        last_message = state["answer"]
        if last_message.tool_calls:
            return "tools"
        return "__end__"


    subgraph.add_conditional_edges("process_message", should_continue)
    subgraph.add_edge("tools", END)
    print(subgraph.compile().get_input_schema())
    return subgraph.compile()