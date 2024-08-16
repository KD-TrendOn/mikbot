from langchain_openai import ChatOpenAI
from typing import Literal
from ..config import settings


def init_chat_model(mode:Literal['light', 'main']):
    if mode=='light':
        return ChatOpenAI(temperature=0.7, model="gpt-4o-mini", openai_api_key=settings.openai_api_key, openai_api_base=settings.openai_base_provider)
    return ChatOpenAI(temperature=0.7, model='gpt-4o', openai_api_key=settings.openai_api_key, openai_api_base=settings.openai_base_provider)