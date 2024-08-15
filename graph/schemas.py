from typing import TypedDict, List, Literal, Dict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langchain.pydantic_v1 import BaseModel, Field


class RouterAnswer(BaseModel):
    answer:Literal['accounts', 'cards', 'parking']=Field(description="Points to service which is needed for user's request processing.")


class GraphConfig(TypedDict):
    thread_id: str
    """The thread ID of the conversation."""
    user_id: str
    """The ID of the user to remember in the conversation."""


class State(TypedDict):
    answer:AnyMessage
    user_input:str
    service: str
    user_id: str
    useless:str


class SubState(TypedDict):
    user_input:str
    answer:AnyMessage
    useless:str