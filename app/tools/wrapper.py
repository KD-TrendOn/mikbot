from typing import List, Dict, Any, Callable
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, tool

class ToolWrapper(BaseModel):
    name: str
    description: str
    function: Callable
    input_schema: type[BaseModel]

def create_tool_from_callable(tool_wrapper: ToolWrapper) -> BaseTool:
    # Создаем новую схему ввода, которая включает оригинальные поля и description
    class EnhancedInputSchema(tool_wrapper.input_schema):
        description: str = Field(..., description="Дополнительное описание для пользователя")

    @tool(tool_wrapper.name, args_schema=EnhancedInputSchema)
    def dynamic_tool(**kwargs) -> Dict[str, Any]:
        """
        {description}

        This tool takes the following arguments:
        {args_description}
        """
        # Извлекаем description и передаем остальные аргументы в оригинальную функцию
        description = kwargs.pop('description')
        result = tool_wrapper.function(**kwargs)
        return {
            "result": result,
            "description": description
        }
    
    # Обновляем документацию функции
    args_description = "\n".join([f"- {field}: {field_info.description}" for field, field_info in EnhancedInputSchema.__fields__.items() if field != 'description'])
    dynamic_tool.__doc__ = dynamic_tool.__doc__.format(
        description=tool_wrapper.description,
        args_description=args_description
    )
    
    return dynamic_tool

def create_tools(tools: List[ToolWrapper]) -> List[BaseTool]:
    return [create_tool_from_callable(tool_wrapper) for tool_wrapper in tools]
