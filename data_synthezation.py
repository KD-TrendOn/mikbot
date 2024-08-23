import pandas as pd
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.services.llm import init_chat_model
from datetime import datetime, timezone
import numpy as np
from typing import Literal

numberOfRows = 50

class RowAnswer(BaseModel):
    date:str=Field(description='Дата транзакции строго по формату YYYYMMDD. От 20230823 до 20240823')
    amount:float=Field(description='Сумма расхода в рублях')
    category:Literal["Перевод", "Оплата Продуктовый", "Оплата Аптека","Оплата Ювелирный","Оплата Ресторан","Оплата Развлечения","Онлайн оплата"] = Field(description='Категория расхода строго из списка:"Перевод", "Оплата Продуктовый", "Оплата Аптека","Оплата Ювелирный","Оплата Ресторан","Оплата Развлечения","Онлайн оплата"')

llm = init_chat_model(mode='main')
one_row = [pd.Timestamp('20230823'), 125.15, "Перевод"]
rows = [RowAnswer(date='20230823', amount=125.15, category="Перевод")]
prompt_template = """Ты - оператор расходов пользователя. Твоя задача - создать реалистичное описание расхода пользователя. Ты создатель синтетических данных для таблицы.
Твоя задача заполнить описание о каком то расходе пользователя. Тебе нужно будет указать дату date транзакции по карте, amount - сумма в рублях и consumption_type - категория расходов.
Представь что пользователь обычный человек и тебе нужно придумать одного из его повседневных расходов. Данные придумывай случайные, и тебе еще будет дана информация о его прошлой транзакции.
Так что для новой транзакции выбирай дату буквально на пару тройку дней после представленной транзакции. Выбирай любую категорию и сумму которая тебе кажется адекватной.
Предыдущий расход: {ldate} {lamount} {lcategory}
Отвечать ты должен в строгом формате:
{format_instructions}"""
prompt = PromptTemplate.from_template(prompt_template)
output_parser = PydanticOutputParser(pydantic_object=RowAnswer)
format_instructions = output_parser.get_format_instructions()
bound = prompt | llm | output_parser

rdf = pd.DataFrame(columns=["date", "amount", "category"])
rdf.loc[0] = one_row
print(rdf)
rdf.to_csv('data.csv', index=False)

for i in range(1, numberOfRows):
    response = bound.invoke({"ldate":rows[-1].date, "lamount":rows[-1].amount, 'lcategory':rows[-1].category, "format_instructions":format_instructions})
    rows.append(response)
    print(response)
    
    new_row = pd.DataFrame([[pd.Timestamp(response.date), response.amount, response.category]], 
                           columns=["date", "amount", "category"])
    rdf = pd.concat([rdf, new_row], ignore_index=True)
    
    rdf.to_csv("data.csv", index=False)

print(rdf)
print(rdf.dtypes)
print(rdf)
print(rdf.dtypes)