import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table
import os

engine = create_engine('mysql://samrullo:18Aranid@jspandabusiness.crrz64gldft9.ap-south-1.rds.amazonaws.com/jspanda?charset=utf8')

folder = r'C:\Users\amrul\Documents\japan_sweets_business'
file = 'jspanda_stock.xlsx'

df = pd.read_excel(os.path.join(folder, file), encoding="utf-8")

df.columns = ['name', 'quantity', 'category', 'price']

stock_df = df[['name', 'quantity']].copy()
stock_df = stock_df.fillna("")
stock_df['quantity'] = pd.to_numeric(stock_df['quantity'])

product_df = pd.read_sql("select * from product", engine)
print("insert stock")

statement = "INSERT INTO `stock`(`product_id`,`quantity`) VALUES (%s,%s,)"

metadata = MetaData()
stock_tbl = Table("stock", metadata, autoload=True, autoload_with=engine)
con = engine.connect()
for i, row in stock_df.iterrows():
    print(f"Will insert {i}, {row['name']}")
    product_id = product_df.loc[product_df['name'] == row['name'], 'id'].values[0]
    print(f"product id for {row['name']} is {product_id}")
    insert_values = {'product_id': product_id, 'quantity': row['quantity']}
    stmt = stock_tbl.insert().values(insert_values)
    con.execute(stmt)
