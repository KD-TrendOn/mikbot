from typing import List, Dict, Any
from pydantic import BaseModel
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

class ToolWrapper(BaseModel):
    name: str
    description: str
    function: str
    input_schema: Dict[str, Any]

def create_tool_from_db(tool_data: ToolWrapper):
    @tool(tool_data.name, description=tool_data.description, args_schema=tool_data.input_schema)
    def dynamic_tool(**kwargs):
        # Здесь нужно реализовать безопасное выполнение функции из строки
        # Например, используя `exec` с ограниченным глобальным пространством имен
        # Это потенциально опасно и требует дополнительных мер безопасности
        local_vars = {}
        exec(tool_data.function, {}, local_vars)
        return local_vars['result']

    return dynamic_tool

def create_tool_node(tools: List[ToolWrapper]):
    dynamic_tools = [create_tool_from_db(tool) for tool in tools]
    return ToolNode(dynamic_tools)