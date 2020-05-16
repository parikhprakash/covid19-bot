import pandas as pd
import requests

all_data_response = requests.get('https://api.covid19india.org/data.json')
all_data = all_data_response.json()
daily_data = all_data['cases_time_series']

df = pd.DataFrame(daily_data)
df['date'] = df['date'].apply(lambda x: x + '2020')
df['date'] = pd.to_datetime(df['date'],format="%d %B %Y")
for col in df.columns:
    if col != 'date':
        df[col] = pd.to_numeric(df[col])

df['dailyactive'] = df['dailyconfirmed'] - df['dailyrecovered'] - df['dailydeceased']
df['totalactive'] = df['totalconfirmed'] - df['totalrecovered'] - df['totaldeceased']
import pickle
with open('daily_data.pkl','wb') as fp:
    pickle.dump(df,fp)