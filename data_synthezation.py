import pandas as pd
from typing import Literal
import random
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
        return {"chartPieConfig":{"value":{"label":"Рублей"}},"data":data,"type":"chartPie"}
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
        return {"chartPieConfig":{"value":{"label":"Рублей"}},"data":data,"type":"chartPie"}

print(pie_chart(data_type='Expense', time_period='all_time'))