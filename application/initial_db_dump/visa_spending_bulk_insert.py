import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))

folder = r'C:\Users\amrul\Documents\japan_sweets_business'
file = 'japansweet_business_hisob_kitob.xlsx'

yahoo_df = pd.read_excel(os.path.join(folder, file), sheet_name=1)
yahoo_df['visa'] = 'yahoo'
costco_df = pd.read_excel(os.path.join(folder, file), sheet_name=2)
costco_df['visa'] = 'costco'
rakuten_df = pd.read_excel(os.path.join(folder, file), sheet_name=3)
rakuten_df['visa'] = 'rakuten'
for df in (yahoo_df, costco_df, rakuten_df):
    df.dropna(inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'])

all_df = pd.concat([yahoo_df, costco_df, rakuten_df])
all_df.index = range(len(all_df))
print(f"Visa spendings all loaded and will insert them to visa_spending: {len(all_df)}")

all_df[['date', 'visa', 'amount']].to_sql('visa_spending', engine, index_label='id', if_exists='append')

# print(f"Dataframe loaded : {df.head()}")
#
# print(f"Will insert total of {len(new_df)} records")
#
# new_df.to_sql('shipment_spending', engine, index_label="id", if_exists='append')
