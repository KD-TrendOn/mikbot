import asyncio
import logging
from langgraph.graph import StateGraph, END, START
from ..schemas.state import SubState
from ..services.llm import init_chat_model
from ..database.crud import load_service_data, load_tools, load_vector_documents
from ..tools.wrapper import create_tools
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
logger = logging.getLogger(__name__)

def create_worker_subgraph(service_name: str):
    logger.info(f"Creating worker subgraph for service: {service_name}")
    subgraph = StateGraph(SubState)

    async def load_service_data_node(state: SubState):
        logger.debug(f"Loading service data for {service_name}")
        logger.debug(f"State metadata: {state.metadata}")
        db = state.metadata.get("db")
        if db is None:
            logger.error("Database session is None in load_service_data_node")
            raise ValueError("Database session is not available")
        service_data = await asyncio.create_task(load_service_data(db, service_name))
        logger.debug(f"Service data loaded: {service_data}")
        return {"metadata": {**state.metadata, "service_data": service_data}}

    async def load_tools_node(state: SubState):
        logger.debug(f"Loading tools for {service_name}")
        logger.debug(f"State metadata: {state.metadata}")
        db = state.metadata.get("db")
        if db is None:
            logger.error("Database session is None in load_tools_node")
            raise ValueError("Database session is not available")
        tool_wrappers = await asyncio.create_task(load_tools(db, service_name))
        tools = create_tools(tool_wrappers)
        tool_node = ToolNode(tools)
        
        # Создаем описание инструментов для промпта
        tools_description = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
        
        logger.debug(f"Tools loaded: {[tool.name for tool in tools]}")
        return {"metadata": {**state.metadata, "tools": tools, "tool_node": tool_node, "tools_description": tools_description}}

    async def process_message(state: SubState):
        logger.debug("Processing message")
        service_data = state.metadata.get("service_data")
        tools = state.metadata.get("tools")
        tools_description = state.metadata.get("tools_description")
        vector_docs = state.metadata.get("vector_docs", [])
        
        llm = init_chat_model(mode="main")
        llm_with_tools = llm.bind_tools(tools)
        
        context = "\n".join([doc.page_content for doc, _ in vector_docs])
        
        prompt_template = """You are an assistant for the {service_name} service of the Tatarstan Resident Card application.
        
        Available tools:
        {tools_description}
        
        For each tool, you must provide a 'description' field in addition to the required arguments. 
        This description should be a brief explanation of the action being taken, which will be shown to the user.
        
        Service context:
        {service_data}
        
        Additional context:
        {context}
        
        User input: {user_input}
        
        Please respond to the user's input using the available tools if necessary. 
        Remember to include a meaningful description for each tool use."""
        prompt = PromptTemplate.from_template(prompt_template)
        logger.debug(f"Invoking LLM with prompt: {prompt.format(service_name=service_name, tools_description=tools_description, service_data=service_data.documentation if service_data else 'No service data available', context=context, user_input = state.user_input)}")
        bound = prompt | llm_with_tools
        response = await bound.ainvoke({"service_name":service_name, "tools_description":tools_description, "service_data":service_data.documentation if service_data else 'No service data available', "context":context, "user_input":state.user_input})
        logger.debug(f"LLM response received {response.content}")
        return {"answer": [response], "messages": response}

    async def load_vector_docs_node(state: SubState):
        logger.debug(f"Loading vector documents for query: {state.user_input}")
        docs = await load_vector_documents(service_name, state.user_input)
        logger.debug(f"Vector documents loaded: {len(docs)} documents")
        return {"metadata": {**state.metadata, "vector_docs": docs}}
    

    subgraph.add_node("load_service_data", load_service_data_node)
    subgraph.add_node("load_tools", load_tools_node)
    subgraph.add_node("load_vector_docs", load_vector_docs_node)
    subgraph.add_node("process_message", process_message)

    subgraph.add_edge(START, "load_service_data")
    subgraph.add_edge("load_service_data", "load_tools")
    subgraph.add_edge("load_tools", "load_vector_docs")
    subgraph.add_edge("load_vector_docs", "process_message")

    def should_use_tool(state: SubState):
        logger.debug("Checking if tool should be used")
        last_message = state.messages[-1]
        if last_message.tool_calls:
            logger.debug("Tool call detected")
            return "use_tool"
        logger.debug("No tool call detected")
        return END

    async def use_tool(state: SubState):
        logger.debug(f"Using tool. State at the moment: {state.dict()}")
        tool_node = state.metadata.get("tool_node")
        if tool_node is None:
            logger.error("Tool node is None in use_tool")
            raise ValueError("Tool node is not available")
        tool_input = AIMessage(
            content="",
            tool_calls=state.messages[-1].tool_calls
        )
        tool_results = await tool_node.ainvoke({'messages':[tool_input]})
        
        logger.debug("Processing tool results")
        processed_results = []
        for result in tool_results.get("messages", []):
            if isinstance(result, dict) and "result" in result and "description" in result:
                processed_results.append({
                    "result": result["result"],
                    "description": result["description"]
                })
            else:
                processed_results.append(result)
        
        logger.debug(f"Processed {len(processed_results)} tool results")
        return {'answer':processed_results}

    subgraph.add_node("use_tool", use_tool)

    subgraph.add_conditional_edges(
        "process_message",
        should_use_tool,
        {
            "use_tool": "use_tool",
            END: END
        }
    )
    subgraph.add_edge("use_tool", END)

    logger.info(f"Worker subgraph for {service_name} created successfully")
    return subgraph.compile()
