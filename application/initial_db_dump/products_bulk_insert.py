import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table
import os

engine = create_engine('mysql://samrullo:18Aranid@jspandabusiness.crrz64gldft9.ap-south-1.rds.amazonaws.com/jspanda?charset=utf8')

folder = r'C:\Users\amrul\Documents\japan_sweets_business'
file = 'jspanda_stock.xlsx'

df = pd.read_excel(os.path.join(folder, file), encoding="utf-8")

df.columns = ['name', 'quantity', 'category', 'price']

category_df = pd.read_sql("select * from category", engine)
print("insert products")
# category_df.to_sql("category", engine, index_label="id", if_exists='append')

# new_df.to_sql('jspanda_orders', engine, index_label="id", if_exists="append")
statement = "INSERT INTO `product`(`name`,`price`,`extra_info`,`category_id`) VALUES (%s,%s,%s,%s)"

products_df = df[['name', 'category', 'price']].copy()
print(f"Original products dataframe length : {len(products_df)}")
products_df = products_df.drop_duplicates()
print(f" products dataframe length after dropping duplicates: {len(products_df)}")
products_df['extra_info'] = ""
products_df = products_df.fillna("")

for i, row in products_df.iterrows():
    try:
        products_df.loc[i, 'price'] = float(row['price'])
    except Exception as e:
        print(f"exception occurred with price value {row['price']}")
        products_df.loc[i, 'extra_info'] = row['price']
        products_df.loc[i, 'price'] = 0
        pass

metadata = MetaData()
product_tbl = Table("product", metadata, autoload=True, autoload_with=engine)
con = engine.connect()
for i, row in products_df.iterrows():
    print(f"Will insert {i}, {row['name']}")
    category_id = category_df.loc[category_df['name'] == row['category'], 'id'].values[0]
    print(f"category id for {row['name']} is {category_id}")
    insert_values = {'name': row['name'], 'price': row['price'], 'extra_info': row['extra_info'], 'category_id': category_id}
    stmt = product_tbl.insert().values(insert_values)
    con.execute(stmt)
