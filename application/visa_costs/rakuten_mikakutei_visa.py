import pandas as pd
import numpy as np
import os
import re
import logging

folder = r'C:\Users\amrul\Documents\japan_sweets_business\rakuten_visa_spendings'
file = 'rakuten_201912.csv'
df = pd.read_csv(os.path.join(folder, file), encoding='sjis')
print("loaded data")

orig_cols =['利用日', '利用店名・商品名', '利用者', '支払方法', '利用金額', '支払手数料', '支払総額', '支払月','12月支払金額', '1月繰越残高', '1月以降支払金額']
new_col_names = ['date', 'name', 'user', 'method', 'amount', 'tesuryo', 'total_amount', 'payment_month', 'this_month_amount', 'next_month_balance', 'next_next_month_balance']
df.columns = new_col_names
df['is_mine'] = False

df['final_total_amount'] = df['total_amount']
df['method'] = df['method'].apply(str)
df['is_bunkatsu'] = df['method'].apply(lambda x: re.search('分割', x))
df.loc[np.logical_not(df['is_bunkatsu'].isnull()), 'final_total_amount'] = df.loc[np.logical_not(df['is_bunkatsu'].isnull()), 'this_month_amount']

kazoku_df = df.loc[df['user'] == '家族'].copy()
mine_df = df.loc[df['user'] != '家族'].copy()
print("kazoku records : {}, kazoku amount : {} \n honnin records : {}, honnin amount : {}\n".format(len(kazoku_df), kazoku_df['total_amount'].sum(), len(mine_df), mine_df['total_amount'].sum()))
print("total records: {}, total amount : {}\n".format(len(df), df['final_total_amount'].sum()))

for i, row in mine_df.iterrows():
    if re.search('ＥＴＣ', row['name']) or re.search('MVCI', row['name']) or re.search('ｿﾌﾄﾊﾞﾝｸ', row['name']) or re.search('AIRBNB', row['name']):
        mine_df.loc[i, 'is_mine'] = True

for i, row in kazoku_df.iterrows():
    if re.search('ＥＴＣ', row['name']) or re.search('MVCI', row['name']) or re.search('ｿﾌﾄﾊﾞﾝｸ', row['name']) or re.search('AIRBNB', row['name']):
        kazoku_df.loc[i, 'is_mine'] = True

print("finished is_mine assigning")
not_mine_df = mine_df.loc[np.logical_not(mine_df['is_mine'])]
real_mine_df = pd.concat([mine_df.loc[mine_df['is_mine']].copy(), kazoku_df.loc[kazoku_df['is_mine']].copy()])
kazoku_df=kazoku_df.loc[np.logical_not(kazoku_df['is_mine'])].copy()

print("rakuten mine records : {}\n not mine records out of rakuten mine records : {}".format(len(mine_df), len(not_mine_df)))

dinara_business_items = ['ﾕﾆｸﾛ ｼﾞ-ﾕ- ｵ', 'ユニクロ', 'ＭＥＧＡドン・キホーテ三郷店', 'ららぽーと\u3000新三郷', 'ﾖﾄﾞﾊﾞｼｶﾒﾗ ﾂｳｼﾝﾊﾝ', 'ＭＯＮＯゲートＳＨＯＰ', 'ﾖｳｶﾞ       ｼﾞﾖｳﾊﾞﾝﾄﾞ', 'ｼﾝｺﾞｳﾀﾞｲｲﾁ ﾄｳﾒｲｾﾂｿﾞｸ', 'エナジードラッグ', 'ＬＥＧＳＳＥＶＥＮ靴下専門店', 'ｸﾞﾛｰﾊﾞﾙﾜｲﾌｱｲ ﾋﾞｼ', 'オリエントストア',
                         'スピルリナ普及会\u3000楽天市場店', 'ＦＡＮＣＬ楽天市場店', 'AMAZON.CO.JP  (ﾍﾝｻｲﾍﾝｺｳ', 'おしゃれｃａｆｅ楽天市場店',
                         'ｴﾅｼﾞ-ﾄﾞﾗｯｸﾞ   (ﾍﾝｻｲﾍﾝｺｳ', 'ｼﾝｼﾞﾕｸ     ｼﾊﾞｺｳｴﾝｳﾁ',
                         'ｼﾞﾖｳﾊﾞﾝﾄﾞｳ ﾅｶﾉﾁﾖｳｼﾞﾔ', 'ｼﾊﾞｺｳｴﾝｿﾄ  ｼﾞﾖｳﾊﾞﾝﾄﾞ',
                         'ｽﾋﾟﾙﾘﾅﾌｷｭｳｶｲﾗｸ(ﾍﾝｻｲﾍﾝｺｳ', 'ｶﾍｲﾐﾅﾐ     ﾂﾂﾐﾄﾞｵﾘｳｴ',
                         'ﾄﾞﾗｯｸﾞｽﾄｱｻﾞｸﾞｻ(ﾍﾝｻｲﾍﾝｺｳ', 'ｻﾝﾄﾞﾗｯｸﾞ ｲ-ｼｮｯ(ﾍﾝｻｲﾍﾝｺｳ',
                         'ｱﾝｼﾞｪﾎﾞ-ﾃ     (ﾍﾝｻｲﾍﾝｺｳ']
print("------------------------------------------------------------------")
print("Final total amount : {:,}".format(df['final_total_amount'].sum()))
print("Kazoku total amount :{:,}".format(kazoku_df['final_total_amount'].sum()))
print("Not mine total amount : {:,}".format(not_mine_df['final_total_amount'].sum()))
print("Dinara business total amount : {:,}".format(kazoku_df['final_total_amount'].sum() + not_mine_df['final_total_amount'].sum()))
print("Real mine total amount : {:,}".format(real_mine_df['final_total_amount'].sum()))
