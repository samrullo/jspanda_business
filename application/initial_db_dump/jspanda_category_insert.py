import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table
import os

engine = create_engine('mysql://samrullo:18Aranid@jspandabusiness.crrz64gldft9.ap-south-1.rds.amazonaws.com/jspanda?charset=utf8')

folder = r'C:\Users\amrul\Documents\japan_sweets_business'
file = 'jspanda_stock.xlsx'

df = pd.read_excel(os.path.join(folder, file), encoding="utf-8")

df.columns = ['name', 'quantity', 'category', 'price']

category_df = df[['category']].copy()
category_df = category_df.drop_duplicates()
category_df.index = [i for i in range(len(category_df))]

print("insert categories")
# category_df.to_sql("category", engine, index_label="id", if_exists='append')

# new_df.to_sql('jspanda_orders', engine, index_label="id", if_exists="append")
statement = "INSERT INTO `category`(`name`) VALUES (%s)"

metadata = MetaData()
category_tbl = Table("category", metadata, autoload=True, autoload_with=engine)
con = engine.connect()
for i, row in category_df.iterrows():
    print(f"Will insert {i}, {row['category']}")
    insert_values = {'name': row['category']}
    stmt = category_tbl.insert().values(insert_values)
    con.execute(stmt)
