from typing import List, Dict, Any, Callable
from pydantic import BaseModel
from langchain_core.tools import BaseTool, tool

class ToolWrapper(BaseModel):
    name: str
    description: str
    function: Callable
    input_schema: type[BaseModel]

def create_tool_from_callable(tool_wrapper: ToolWrapper) -> BaseTool:
    @tool(tool_wrapper.name, description=tool_wrapper.description, args_schema=tool_wrapper.input_schema)
    def dynamic_tool(**kwargs) -> Dict[str, Any]:
        result = tool_wrapper.function(**kwargs)
        return {
            "result": result,
            "description": tool_wrapper.description
        }
    
    dynamic_tool.__doc__ = tool_wrapper.function.__doc__
    
    return dynamic_tool

def create_tools(tools: List[ToolWrapper]) -> List[BaseTool]:
    return [create_tool_from_callable(tool_wrapper) for tool_wrapper in tools]
