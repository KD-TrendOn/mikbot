from typing import List, Dict, Any, Optional, Annotated
from pydantic.v1 import BaseModel as VBaseModel, Field as VField, create_model
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

class UserInput(BaseModel):
    user_input: str
    user_id: str

def create_router_answer(service_names: List[str]):
    return create_model(
        'RouterAnswer',
        answer=(str, Field(..., description="Points to service which is needed for user's request processing.")),
        __config__=type('Config', (), {'use_enum_values': True})
    )

# Это будет обновляться при запуске приложения
RouterAnswer = create_router_answer([])