import pandas as pd
import numpy as np
import os
import re
import datetime


def to_yyyymmdd(date):
    return datetime.datetime.strftime(date, "%Y%m%d")


folder = r'C:\Users\amrul\Documents\japan_sweets_business\saison_visa_spendings'
year_month = "202101"
file = f'SAISON_{year_month}.csv'
df = pd.read_csv(os.path.join(folder, file), header=3, encoding="shift-jis")
print(f"loaded data : {len(df)}")

# Index(['利用日', 'ご利用店名及び商品名', '本人・家族区分', '支払区分名称', '締前入金区分', '利用金額', '備考'], dtype='object')
columns = ["date", "name", "who", "split", "yakujomaenyukinkubun", "amount", "extra"]
df.columns = columns
visa_df = df.loc[np.logical_not(df['date'].isnull())]
visa_df['date'] = pd.to_datetime(visa_df['date'])
min_date = visa_df['date'].min()
max_date = visa_df['date'].max()
visa_df.sort_values('amount', ascending=False, inplace=True)
print(visa_df[['date', 'name', 'amount']].to_string())
visa_df.to_excel(os.path.join(folder, f"saison_{to_yyyymmdd(min_date)}_to_{to_yyyymmdd(max_date)}.xlsx"))

# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib
#
# sns.set(font="IPAexGothic")
# g = sns.barplot(x="amount", y="name", data=visa_df)
#
# plt.xlabel("金額", fontname="IPAexGothic")
# plt.ylabel("ショッピング支店", fontname="IPAexGothic")
# plt.show()

grp_df = visa_df.groupby('name')[['amount']].sum()
grp_df = grp_df.sort_values('amount', ascending=False)
for i, row in grp_df.iterrows():
    print(f"{i: <30} : {row['amount']: >10}")

grp_df.to_excel(os.path.join(folder,f"grouped_by_name_{year_month}.xlsx"))
