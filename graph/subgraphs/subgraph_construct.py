from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from typing import TypedDict, List, Literal, Dict
from ..schemas import State
from .model_init import init_chat_model
# Создание подграфа для работника
def create_worker_subgraph(worker_name: str, worker_tools: List[tool]):
    
    
    async def load_service_docs(state: State, config: RunnableConfig) -> State:
        # Здесь должна быть логика загрузки документации для выбранного сервиса
        return {"service_docs": f"{worker_name} documentation placeholder"}


    async def load_bot_docs(state: State, config: RunnableConfig) -> State:
        # Здесь должна быть логика загрузки документации бота
        return {"bot_docs": f"{worker_name} bot documentation placeholder"}


    async def process_message(state: State, config: RunnableConfig) -> State:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful banking assistant. Use the provided information to answer the user's question or call an appropriate tool."),
            ("human", "{user_input}"),
            ("system", "Service documentation: {service_docs}"),
            ("system", "Bot documentation: {bot_docs}")
        ])
        chain = prompt | init_chat_model(mode="main").bind(tools=worker_tools)
        response = await chain.ainvoke({
            "user_input": state["user_input"],
            "service_docs": state["service_docs"],
            "bot_docs": state["bot_docs"]
        })
        return {"answer": response.content, "tool_calls": response.additional_kwargs.get("tool_calls", [])}


    subgraph = StateGraph(State)
    subgraph.add_node("load_service_docs", load_service_docs)
    subgraph.add_node("load_bot_docs", load_bot_docs)
    subgraph.add_node("process_message", process_message)
    subgraph.add_node("tools", ToolNode(worker_tools))


    subgraph.set_entry_point("load_service_docs")
    subgraph.add_edge("load_service_docs", "load_bot_docs")
    subgraph.add_edge("load_bot_docs", "process_message")


    def route_tool_or_end(state: State) -> Literal["tools", "__end__"]:
        return "tools" if state.get("tool_calls") else "__end__"


    subgraph.add_conditional_edges("process_message", route_tool_or_end)
    subgraph.add_edge("tools", END)

    return subgraph.compile()