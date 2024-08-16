from typing import List, Dict, Any, Literal, Annotated
from pydantic import BaseModel
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class State(BaseModel):
    messages: Annotated[List[AnyMessage], add_messages]
    service: str
    user_input: str
    answer: Any
    user_id: str
    metadata: Dict[str, Any] = {}

class SubState(BaseModel):
    messages: Annotated[List[AnyMessage], add_messages]
    user_input: str
    answer: Any
    service_id: str
    metadata: Dict[str, Any] = {}

class RouterOutput(BaseModel):
    service: Literal['accounts', 'cards', 'parking', 'legal_assistant']