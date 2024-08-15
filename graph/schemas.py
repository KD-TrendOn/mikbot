from typing import TypedDict, List, Literal, Dict
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langchain.pydantic_v1 import BaseModel, Field


class RouterAnswer(BaseModel):
    answer:Literal['accounts', 'cards', 'parking']=Field(description="Points to service which is needed for user's request processing.")


class GraphConfig(TypedDict):
    thread_id: str
    """The thread ID of the conversation."""
    user_id: str
    """The ID of the user to remember in the conversation."""


class State(TypedDict):
    messages: List[AnyMessage, add_messages]
    user_input: str
    service: str
    service_docs: str
    tool_calls:list
    bot_docs: str
    answer: str
    user_id: str
    tool_result: str

