import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table
import os

engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))

folder = r'C:\Users\amrul\Documents\programming\japansweet'
file = 'jspanda_orders_20181210_to_20191101.xlsx'

cols = ['date', 'name', 'quantity', 'price', 'selling_price_per_unit', 'total_cost', 'order_sum', 'ordered_by', 'extra_notes', 'is_paid']

df = pd.read_excel(os.path.join(folder, file), parse_dates=True, encoding="utf-8")
df['total_cost'] = df['price'] * df['quantity']
df['order_sum'] = df['selling_price_per_unit'] * df['quantity']
df['is_paid'] = True
df['date'] = df['adate']
df['extra_notes'] = ""

new_df = df[cols].copy()
print(new_df.head())

new_df.index = [i for i in range(len(new_df))]
# new_df.loc[new_df['ordered_by'] == 'на продажу', 'ordered_by'] = "na_prodaju"
new_df['ordered_by'] = new_df['ordered_by'].str.encode("utf-8")
new_df['extra_notes'] = new_df['extra_notes'].str.encode("utf-8")
new_df['name'] = new_df['name'].str.encode("utf-8")

# new_df.to_sql('jspanda_orders', engine, index_label="id", if_exists="append")
statement = "INSERT INTO `jspanda_orders`(`date`,`quantity`,`price`,`selling_price_per_unit`,`total_cost`,`order_sum`,`ordered_by`,`extra_notes`,`is_paid`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

# get rid of nan values
new_df['ordered_by'] = new_df['ordered_by'].fillna("")
new_df['extra_notes'] = new_df['extra_notes'].fillna("")
new_df['name'] = new_df['name'].fillna("NOPRODUCTNAME")

metadata = MetaData()
jspanda_orders_tbl = Table("jspanda_orders", metadata, autoload=True, autoload_with=engine)
con = engine.connect()
for i, row in new_df.iterrows():
    print(f"Will insert {i}, {row['name']}")
    insert_values = {}
    for key in new_df.columns:
        insert_values[key] = row[key]
    stmt = jspanda_orders_tbl.insert().values(insert_values)
    con.execute(stmt)
