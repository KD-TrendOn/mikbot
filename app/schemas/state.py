from typing import List, Dict, Any, Optional, Annotated
from pydantic.v1 import BaseModel as VBaseModel, Field as VField
from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from ..database.models import ChatMessage

class State(VBaseModel):
    messages: Annotated[List[AnyMessage], add_messages] = VField(default_factory=list)
    service: Optional[str] = None
    user_input: str
    answer: Any = None
    user_id: str
    metadata: Dict[str, Any] = VField(default_factory=dict)
    chat_history: list = VField(default_factory=list)

class SubState(VBaseModel):
    messages: Annotated[List[AnyMessage], add_messages] = VField(default_factory=list)
    user_input: str
    answer: Any = None
    service: Optional[str] = None
    metadata: Dict[str, Any] = VField(default_factory=dict)
    chat_history: list = VField(default_factory=list)

class RouterOutput(VBaseModel):
    service: str

class UserInput(BaseModel):
    user_input: str
    user_id: str
