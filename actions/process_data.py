import pandas as pd
import requests
from datetime import datetime

def update_pickles():
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


    district_data_response = requests.get('https://api.covid19india.org/districts_daily.json')  
    district_datewise = district_data_response.json() 

    daily_data = district_datewise['districtsDaily'] 
    arr_records = []
    for state_keys in daily_data:
        for district_keys in daily_data[state_keys]:
            record = daily_data[state_keys][district_keys]
            for r in record:
                r['state']  = state_keys
                r['district'] = district_keys
                arr_records.append(r)

    df_district = pd.DataFrame(arr_records)
    with open('daily_district.pkl','wb') as fp:
        pickle.dump(df_district,fp)
    dt_update = datetime.today()
    with open('last_updated.pkl','wb') as fdt:
        pickle.dump(dt_update, fdt)   


