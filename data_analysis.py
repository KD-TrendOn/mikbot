import pandas as pd
df = pd.read_csv('ddata.csv')
#    print((pd.Timestamp("20230823") + pd.Timedelta(days=45)).__str__()[:10], 1)
#    print(df.describe())
#    print(len(df['category'].unique()))
#    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
#    for i in df['category'].unique():
#        print(i, int(df[(df['category'] == i) & (df['date'] >= pd.Timestamp('20240201'))]['amount'].sum()))
for i in df['category'].unique():
    print(i, int(df[df['category'] == i]['amount'].sum()))