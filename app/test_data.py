from typing import Dict
from pydantic import BaseModel, Field
from .tools.wrapper import ToolWrapper
from typing import Literal
import pandas as pd
import random


class EmptyInput(BaseModel):
    user_id: str = Field(..., description="ID пользователя")

class SupportInput(BaseModel):
    user_id: str = Field(..., description="ID пользователя")
    message: str = Field(..., description="Сообщение в техподдержку на которое ты не смог ответить")

class PieChartInput(BaseModel):
    data_type: Literal["Income", "Expense"] = Field(..., description="Раздел транзакций пользователя по которому будет построен график.Только 'Income' или 'Expense'")
    time_period: Literal["last_month", "all_time"] = Field(..., description="Временной период для статистики. Опции: 'last_month', 'all_time'")

class LineChartInput(BaseModel):
    user_id : str = Field(..., description='ID пользователя')

class SummaryTableInput(BaseModel):
    data_type: Literal["All", "Income", "Expense"] = Field(..., description='Раздел транзакций пользователя по которому будет показана статистика. На выбор "All", "Income", "Expense"')

def balance_replenishment_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с пополнением баланса карты

    Args:
        user_id (str): _description_

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Пополнение баланса","type":"button","buttonBody":"Отправить"}

def transfer_payment_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с Переводом на другую карту

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Перевод и оплата","type":"button","buttonBody":"Отправить"}

def card_info_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с информацией по банковской карте

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Информация по карте","type":"button","buttonBody":"Отправить"}

def kindergarten_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой детского сада

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Платеж детский сад","type":"button","buttonBody":"Отправить"}

def communal_services_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой ЖКХ

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Платеж ЖКХ","type":"button","buttonBody":"Отправить"}

def public_transport_card_replenishment_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой транспортной карты

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Платеж Транспортная карта","type":"button","buttonBody":"Отправить"}

def educational_card_replenishment_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой образовательной карты 

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Платеж Образовательная карта","type":"button","buttonBody":"Отправить"}

def home_gas_payment_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой Газа по штрих коду

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Платеж Газ по штрих коду","type":"button","buttonBody":"Отправить"}

def traffic_fine_payment_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой штрафов ГИБДД

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Платеж Штрафы ГИБДД","type":"button","buttonBody":"Отправить"}

def taxes_payment_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с оплатой налогов и штрафов

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Платеж Налоги, штрафы","type":"button","buttonBody":"Отправить"}

def internet_replenishment_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с пополнением интернет провайдера

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Платеж Интернет","type":"button","buttonBody":"Отправить"}

def library_card_button(user_id:str):
    """Отправляет пользователю быструю кнопку отсылающую его на страницу с читательским билетом

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Читательский Билет","type":"button","buttonBody":"Отправить"}

def contact_tech_support(user_id:str, message:str):
    """Отправляет запрос на который тебе сложно было ответить в обращение в техподдержку

    Args:
        user_id (str): ID пользователя
        message (str): сообщение пользователя

    Returns:
        Dict: результат во фронтенд
    """
    return {"url":"https://youtu.be/dQw4w9WgXcQ?si=kqouW7rK3vCMOzT6", "header":"Ваш запрос направлен в тех поддержку.","buttonBody":"Отправить","type":"button"}

def pie_chart(data_type: Literal["Income", "Expense"], time_period: Literal["last_month", "all_time"]):
    """Генерирует удобный pie график по какому то срезу транзакций пользователя

    Args:
        data_type (Literal[&quot;Income&quot;, &quot;Expense&quot;]): Income or Expense - раздел транзакций
        time_period (Literal[&quot;last_month&quot;, &quot;all_time&quot;]): Временной период

    Returns:
        Dict: результат во фронтенд
    """
    if data_type == "Income":
        df = pd.read_csv("ddata.csv")
        number_of_colors = len(df["category"].unique())
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
        print(color)
        df['date'] = pd.to_datetime(df['date'])
        if time_period=="all_time":
            data = [{'object':i, 'value':int(df[df['category']==i]['amount'].sum()), "fill":("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))} for i in df['category'].unique()]
        else:
            data = [{'object':i, 'value':int(df[(df['category'] == i) & (df['date'] >= pd.Timestamp('20240406'))]['amount'].sum()), "fill":("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))} for i in df['category'].unique()]
        return {"chartPieConfig":{"value":{"label":"Рублей"}},"chartPieData":data,"type":"chartPie"}
    else:
        df = pd.read_csv("data.csv")
        number_of_colors = len(df["category"].unique())
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
        print(color)
        df['date'] = pd.to_datetime(df['date'])
        if time_period=="all_time":
            data = [{'object':i, 'value':int(df[df['category']==i]['amount'].sum()), "fill":("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))} for i in df['category'].unique()]
        else:
            data = [{'object':i, 'value':int(df[(df['category'] == i) & (df['date'] >= pd.Timestamp('20240406'))]['amount'].sum()), "fill":("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))} for i in df['category'].unique()]
        return {"chartPieConfig":{"value":{"label":"Рублей"}},"chartPieData":data,"type":"chartPie"}


def line_chart(user_id: str):
    """Генерирует удобный линейный график баланса пользователя. Помогает отследить тенденцию баланса пользователя.

    Args:
        user_id (str): ID пользователя

    Returns:
        Dict: результат во фронтенд
    """
    df = pd.read_csv("data.csv")
    rdf = pd.read_csv("ddata.csv")
    df['date'] = pd.to_datetime(df['date'])
    rdf['date'] = pd.to_datetime(rdf['date'])
    data = []
    for i in range(281):
        data.append({"date":(pd.Timestamp("20230823") + pd.Timedelta(days=i)).__str__()[:10], "value":int(rdf[rdf["date"] <= (pd.Timestamp("20230823") + pd.Timedelta(days=i))]["amount"].sum() - df[df["date"] <= (pd.Timestamp("20230823") + pd.Timedelta(days=i))]["amount"].sum())})
    return {"inputChartConfig":{"characteristic":"Рублей на балансе"}, "LineChartData":data, "type":"chartLine"}
