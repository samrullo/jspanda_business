import numpy as np
import pandas as pd
import os
import datetime

folder = r'C:\Users\amrul\Documents\japan_sweets_business\amazon_visa_spendings'
file = 'amazon_kakutei_202211.csv'
# df = pd.read_excel(os.path.join(folder, file), dtype={'ご利用日': str, 'ご利用先など': str, '支払開始': str})

raw_df = pd.read_csv(os.path.join(folder, file), skiprows=1, skipfooter=1, encoding='shift-jis')
raw_df = raw_df.drop('Unnamed: 6', axis=1)
header = list(raw_df.columns)
raw_df.columns = ['date', 'name', 'usage_amount', 'payment_section', 'this_time', 'amount']
raw_df.loc[len(raw_df)] = header
raw_df = raw_df[np.logical_not(raw_df['name'].isnull())]
raw_df['amount'] = pd.to_numeric(raw_df['amount'])
raw_df['amount'] = raw_df['amount'].fillna(0)

print(f"Total : {raw_df['amount'].sum():,.1f}")
print(f"{raw_df.groupby('name')['amount'].sum()}")
