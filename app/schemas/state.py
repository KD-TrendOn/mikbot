from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage

class State(BaseModel):
    messages: List[AnyMessage] = Field(default_factory=list)
    service: Optional[str] = None
    user_input: str
    answer: Any = None
    user_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SubState(BaseModel):
    messages: List[AnyMessage] = Field(default_factory=list)
    user_input: str
    answer: Any = None
    service: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RouterOutput(BaseModel):
    service: str

class UserInput(BaseModel):
    user_input: str
    user_id: str
