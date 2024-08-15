from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from typing import TypedDict, List, Literal, Dict
from .schemas import State
from .service_router import service_router
from .subgraphs import accounts_subgraph, cards_subgraph, parking_subgraph

# Основной граф
main_graph = StateGraph(State)
main_graph.add_node("service_router", service_router)
main_graph.add_node("accounts", accounts_subgraph)
main_graph.add_node("cards", cards_subgraph)
main_graph.add_node("parking", parking_subgraph)


main_graph.add_edge(START, "service_router")


def route_to_service(state: State) -> Literal["accounts", "cards", "parking"]:
    return state["service"]


main_graph.add_conditional_edges("service_router", route_to_service)
main_graph.add_edge("accounts", END)
main_graph.add_edge("cards", END)
main_graph.add_edge("parking", END)

graph_runtime = main_graph.compile()