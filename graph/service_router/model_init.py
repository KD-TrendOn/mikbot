from langchain_openai import ChatOpenAI
from typing import Literal

def init_chat_model(mode:Literal['light', 'main']):
    if mode=='light':
        return ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
    return ChatOpenAI(temperature=0.7, model='gpt-4o')