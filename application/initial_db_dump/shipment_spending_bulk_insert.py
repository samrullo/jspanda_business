import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))

folder = r'C:\Users\amrul\Documents\japan_sweets_business'
file = 'japansweet_business_hisob_kitob.xlsx'

df = pd.read_excel(os.path.join(folder, file), sheet_name=4)
df = df.dropna()
df['date'] = pd.to_datetime(df['date'])
df['shipment_spendings'] = pd.to_numeric(df['shipment_spendings'])
df['weight'] = pd.to_numeric(df['weight'])
new_df = pd.DataFrame(columns=['date', 'weight', 'amount'])
new_df['date'] = df['date']
new_df['weight'] = df['weight']
new_df['amount'] = df['shipment_spendings']

print(f"Dataframe loaded : {df.head()}")

print(f"Will insert total of {len(new_df)} records")

new_df.to_sql('shipment_spending', engine, index_label="id", if_exists='append')
