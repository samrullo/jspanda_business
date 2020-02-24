import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table
import os
import datetime
import sys
import logging
from application.jspanda_orders_from_google.jspanda_orders_gspread import GoogleSpreadsheetToDataframe

logging.basicConfig()

engine = create_engine('mysql://samrullo:18Aranid@jspandabusiness.crrz64gldft9.ap-south-1.rds.amazonaws.com/jspanda?charset=utf8')

gdoc_name = "Товары в наличии"
gdoc_sheet_name = "Основной в наличии "

g_docs_obj = GoogleSpreadsheetToDataframe()
raw_df = g_docs_obj.get_worksheet_as_dataframe(gdoc_name, gdoc_sheet_name)
raw_df = raw_df.iloc[:, :6]
raw_df.columns = ['name', 'quantity', 'category', 'price', 'extra_info','extra_info2']
# raw_df.columns = ['name', 'quantity', 'category', 'price']
raw_df['quantity'] = pd.to_numeric(raw_df['quantity'])
raw_df['quantity'] = raw_df['quantity'].fillna(0)

# statement = "update `stock` set quantity"

product_df = pd.read_sql("select * from product", engine)
stock_df = pd.read_sql("select * from stock", engine)
category_df = pd.read_sql("select * from category", engine)

metadata = MetaData()
stock_tbl = Table("stock", metadata, autoload=True, autoload_with=engine)
product_tbl = Table('product', metadata, autoload=True, autoload_with=engine)
category_tbl = Table('category', metadata, autoload=True, autoload_with=engine)
con = engine.connect()
non_registered_products = []
for i, row in raw_df.iterrows():
    print(f"Will look for product with name {row['name']}")
    if len(product_df.loc[product_df['name'] == row['name'], 'id']) > 0:
        product_id = product_df.loc[product_df['name'] == row['name'], 'id'].values[0]
        if len(stock_df.loc[stock_df['product_id'] == product_id]) > 0:
            if stock_df.loc[stock_df['product_id'] == product_id, 'quantity'].values[0] != row['quantity']:
                print(f"Will update product with id {product_id}, with name {row['name']} to quantity {row['quantity']}")
                # insert_values = {'product_id': product_id, 'quantity': row['quantity']}
                stmt = stock_tbl.update().where(stock_tbl.c.product_id == product_id).values({'quantity': row['quantity']})
                con.execute(stmt)
            else:
                print(f"Quantity of {product_id}:{row['name']} hasn't changed so will skip it")
        else:
            print(f"{product_id} product id {row['name']} product has no stock record. Will insert new stock record")
            stmt = stock_tbl.insert().values({'product_id': product_id, 'quantity': row['quantity']})
            con.execute(stmt)
            print(f"Finished adding {product_id} {row['name']} stock record of {row['quantity']} quantity")
    else:
        print(f"{row['name']} product is not registered yet")
        category_id = 99
        if len(category_df.loc[category_df['name'] == row['category']]) > 0:
            category_id = category_df.loc[category_df['name'] == row['category'], 'id'].values[0]
            print(f"{row['name']} product's category id already exists and it is {category_id}")
        else:
            print("###############################")
            print(f"Will insert new category {row['category']}")
            stmt = category_tbl.insert().values({'name': row['category']})
            con.execute(stmt)
            category_df = pd.read_sql("select * from category", engine)
            category_id = category_df.loc[category_df['name'] == row['category'], 'id'].values[0]
            print(f"Finished inserting new category {row['category']} and its category id is {category_id}")
        stmt = product_tbl.insert().values({'name': row['name'], 'price': row['price'], 'category_id': category_id})
        con.execute(stmt)
        print(f"Finished inserting new product {row['name']}")
        product_df = pd.read_sql("select * from product", engine)
        new_product_id = product_df.loc[product_df['name'] == row['name'], 'id'].values[0]
        stmt = stock_tbl.insert().values({'product_id': new_product_id, 'quantity': row['quantity']})
        con.execute(stmt)
        print(f"Finished adding {new_product_id} {row['name']} stock record of {row['quantity']} quantity")
        non_registered_products.append(i)

print("##################################################################################################################")
print(f"List of products not registered yet : \n {raw_df.loc[non_registered_products].to_string()}")

stock_product_query = """SELECT p.name product_name, s.* FROM stock s, product p WHERE s.product_id=p.id"""
stock_product_df = pd.read_sql(stock_product_query, engine)

product_not_in_stock_scope_df = stock_product_df.loc[np.logical_not(stock_product_df['product_name'].isin(raw_df['name']))]
print(f"There are total of {len(product_not_in_stock_scope_df)} products not in stock scope, will remove them")
for i, row in product_not_in_stock_scope_df.iterrows():
    print(f"Will remove stock record for {row['product_name']}")
    stmt = stock_tbl.delete().where(stock_tbl.c.product_id == row['product_id'])
    con.execute(stmt)
    print(f"Finished removing {row['product_name']} stock record")
