from langchain_openai import ChatOpenAI
from typing import Literal
from ..config import settings


def init_chat_model(mode:Literal['light', 'main']):
    if mode=='light':
        return ChatOpenAI(temperature=settings.LLM_TEMPERATURE, model="gpt-4o-mini", openai_api_key=settings.OPENAI_API_KEY, openai_api_base=settings.OPENAI_BASE_PROVIDER)
    return ChatOpenAI(temperature=settings.LLM_TEMPERATURE, model='gpt-4o', openai_api_key=settings.OPENAI_API_KEY, openai_api_base=settings.OPENAI_BASE_PROVIDER)