# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 21:15:58 2018

@author: amrul
"""
import pandas as pd
import os
import datetime

folder = r'C:\Users\amrul\Documents\japan_sweets_business\costco_visa_spendings'
file = 'costco_visa_202003.xlsx'
# df = pd.read_excel(os.path.join(folder, file), dtype={'ご利用日': str, 'ご利用先など': str, '支払開始': str})
raw_df = pd.read_excel(os.path.join(folder, file), parse_dates=True)
df = raw_df[['ご利用日', 'ご利用先など', 'ご利', '支払', '支払.1', '支払開始', 'ご利用金額', '手数料・利息']].copy()
cols = ['date', 'name', 'who', 'payment_method', 'payment_times', 'payment_start_year_month', 'payed_amount', 'interest']
df.columns = cols
df['used_date'] = pd.TimedeltaIndex(df['date'], unit='d') + datetime.datetime(1900, 1, 1)
df['payed_amount'] = df['payed_amount'].str.replace('円', '')
df['payed_amount'] = df['payed_amount'].str.replace(',', '')
df['payed_amount'] = pd.to_numeric(df['payed_amount'])
print("Total:{:,}".format(df['payed_amount'].sum()))
# ['ご利用日', 'ご利用先など', 'ご利', '支払', '支払.1', '支払開始', 'ご利用金額', '手数料・利息']

# Index(['利用日', 'ご利用先など', 'ご利', '今回', 'ご利用金額', '手数料・利息', 'その他', '当月', 'amount'], dtype='object')
print("Total(family spent):{:,}".format(df.loc[df['who'] == '家族', 'payed_amount'].sum()))

dinara_df = df.loc[df['who'] == '家族'].copy()
mine_df = df.loc[df['who'] != '家族'].copy()

costco_wholesale_df = dinara_df.loc[dinara_df.name == 'コストコ　ホールセール　ジャパン'].copy()
costco_wholesale_df['payed_amount'] = costco_wholesale_df['payed_amount'] * 0.9
dinara_df = dinara_df.drop(costco_wholesale_df.index.tolist())

print(f"breakdown by start year month : \n {df.groupby('payment_start_year_month').sum()['payed_amount']}")

print("---------------------------------------------------------")
print(f"real dinara business : {dinara_df.payed_amount.sum()}")
print(f"costco wholesale : {costco_wholesale_df.payed_amount.sum()}")
print(f"mine : {mine_df.payed_amount.sum()}")
print(f"total mine : {costco_wholesale_df.payed_amount.sum() + mine_df.payed_amount.sum()}")
print(f"total costco card spending : {df.payed_amount.sum()}")
print("---------------------------------------------------------")