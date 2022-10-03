import numpy as np
import pandas as pd
import os
import datetime

folder = r'C:\Users\amrul\Documents\japan_sweets_business\yahoo_visa_spendings'
file = 'yahoo_202207.csv'
# df = pd.read_excel(os.path.join(folder, file), dtype={'ご利用日': str, 'ご利用先など': str, '支払開始': str})

# raw_df = pd.read_csv(os.path.join(folder, file) , skiprows=1, skipfooter=1, encoding='shift-jis')
raw_df = pd.read_csv(os.path.join(folder, file), encoding="shift-jis")
raw_df = raw_df.rename(columns={'利用日': "date", '利用店名・商品名': "name", '利用者': "user", '支払区分': "kubun", '利用金額': "used_amount", '手数料': "fee", '支払総額': "amount", '当月支払金額': "this_month_paid_amount", '翌月以降繰越金額': "next_month_transfer"})
header = list(raw_df.columns)
dinara_shopping_names = ["ｶﾝﾕﾄﾞﾛﾂﾌﾟｵﾝﾗｲﾝｼﾖ"]
raw_df = raw_df[np.logical_not(raw_df['name'].isnull())]
raw_df['amount'] = pd.to_numeric(raw_df['amount'])
raw_df['amount'] = raw_df['amount'].fillna(0)
not_mine_df = raw_df[raw_df["user"].map(lambda user: "本人" not in user)]
mine_df = raw_df[raw_df["user"].map(lambda user: "本人" in user)]
dinara_in_mine_df = mine_df[mine_df["name"].map(lambda shopping_name: any([_name in shopping_name for _name in dinara_shopping_names]))]
dinara_df=pd.concat([not_mine_df,dinara_in_mine_df])
print(f"Total : {raw_df['amount'].sum():,.1f}")
print(f"Not mine : {not_mine_df['amount'].sum():,.1f}")
print(f"Dinara total : {dinara_df['amount'].sum():,.1f}")
print(f"Mine : {mine_df['amount'].sum():,.1f}")
print(f"{raw_df.groupby('name')['amount'].sum()}")
