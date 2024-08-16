from langgraph.graph import StateGraph, END, START
from ..schemas.state import SubState
from ..services.llm import init_chat_model
from ..database.crud import load_service_data, load_tools, load_vector_documents
from ..tools.wrapper import create_tool_node

def create_worker_subgraph(service_name: str):
    subgraph = StateGraph(SubState)

    async def load_service_data_node(state: SubState):
        service_data = await load_service_data(state.metadata["db"], service_name)
        return {"metadata": {"service_data": service_data}}

    async def load_tools_node(state: SubState):
        tools = await load_tools(state.metadata["db"], service_name)
        return {"metadata": {"tools": tools}}

    async def load_vector_docs_node(state: SubState):
        docs = await load_vector_documents(service_name, state.user_input)
        return {"metadata": {"vector_docs": docs}}

    async def process_message(state: SubState):
        service_data = state.metadata["service_data"]
        tools = state.metadata["tools"]
        vector_docs = state.metadata.get("vector_docs", [])
        
        llm = init_chat_model(mode="main")
        llm_with_tools = llm.bind_tools(tools)
        
        context = "\n".join([doc.page_content for doc, _ in vector_docs])
        
        response = await llm_with_tools.ainvoke({
            "service_data": service_data,
            "context": context,
            "user_input": state.user_input,
        })
        
        return {"answer": response, "messages": [response]}

    subgraph.add_node("load_service_data", load_service_data_node)
    subgraph.add_node("load_tools", load_tools_node)
    subgraph.add_node("load_vector_docs", load_vector_docs_node)
    subgraph.add_node("process_message", process_message)
    subgraph.add_node("tools", create_tool_node())

    subgraph.add_edge(START, "load_service_data")
    subgraph.add_edge("load_service_data", "load_tools")
    subgraph.add_edge("load_tools", "load_vector_docs")
    subgraph.add_edge("load_vector_docs", "process_message")

    def should_use_tool(state: SubState):
        last_message = state.messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    subgraph.add_conditional_edges(
        "process_message",
        should_use_tool,
        {
            "tools": "tools",
            END: END
        }
    )
    subgraph.add_edge("tools", "process_message")

    return subgraph.compile()