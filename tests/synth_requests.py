from langchain_core.prompts import PromptTemplate
import re
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from _settings import SETTINGS

llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-4o-mini",
    openai_api_key=SETTINGS.openai_api_key,
    openai_api_base=SETTINGS.openai_base_provider,
)


def generate_requests(tool, tool_name: str, num_requests=100):
    prompt = PromptTemplate(
        input_variables=["tool_name", "tool_description"],
        template="""Создайте {num_requests} реалистичных пользовательских запросов для инструмента "{tool_name}".

            Описание инструмента: {tool_description}

            Правила:
            - Каждый запрос должен начинаться с новой строки
            - Не используйте нумерацию или маркеры перед запросами
            - Избегайте вступлений, описаний или пояснений
            - Запросы должны быть разнообразными и охватывать различные аспекты использования инструмента

            Пример формата:
            Использовать X для Y
            Могу ли я выполнить X
            Хочу сделать X для моего Y
            Завтра сделай X в Y часов
            

            Запросы:
            """,
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    tool_description = tool.__doc__

    all_requests = []
    while len(all_requests) < num_requests:
        response = chain.run(
            tool_name=tool_name,
            tool_description=tool_description,
            num_requests=min(20, num_requests - len(all_requests)),
        )
        requests = response.strip().split("\n")
        all_requests.extend(requests)

    return all_requests[:num_requests]
