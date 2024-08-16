from pydantic import BaseModel, Field
from typing import Any, Dict, Callable
from langchain_core.tools import tool

class ToolInput(BaseModel):
    pass

class ToolOutput(BaseModel):
    result: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BaseTool:
    def __init__(self, func: Callable, name: str, description: str):
        self.func = func
        self.name = name
        self.description = description

    def __call__(self, **kwargs) -> ToolOutput:
        result = self.func(**kwargs)
        return ToolOutput(result=result)

    @classmethod
    def from_function(cls, func: Callable, name: str, description: str):
        return cls(func, name, description)

def create_tool(func: Callable, name: str, description: str, input_schema: type[ToolInput]):
    @tool(name, description=description, args_schema=input_schema)
    def wrapped_tool(**kwargs) -> Dict[str, Any]:
        tool_instance = BaseTool.from_function(func, name, description)
        output = tool_instance(**kwargs)
        return {"result": output.result, "metadata": output.metadata}

    return wrapped_tool