import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table
import os
import datetime
import sys
from application.utils.utils import get_logger
from application.jspanda_orders_from_google.jspanda_orders_gspread import GoogleSpreadsheetToDataframe

logger = get_logger()

engine = create_engine('mysql://samrullo:18Aranid@jspandabusiness.crrz64gldft9.ap-south-1.rds.amazonaws.com/jspanda?charset=utf8')

gdoc_name = "Товары в наличии"
gdoc_sheet_name = "Лист1"

adate = datetime.date(2019, 11, 8)

g_docs_obj = GoogleSpreadsheetToDataframe()
raw_df = g_docs_obj.get_worksheet_as_dataframe(gdoc_name, gdoc_sheet_name)
raw_df.columns = ['name', 'quantity', 'category', 'price', 'extra_info']
raw_df['quantity'] = pd.to_numeric(raw_df['quantity'])
raw_df['quantity'] = raw_df['quantity'].fillna(0)

# statement = "update `stock` set quantity"

product_df = pd.read_sql("select * from product", engine)
stock_df = pd.read_sql("select * from stock", engine)

metadata = MetaData()
stock_tbl = Table("stock", metadata, autoload=True, autoload_with=engine)
con = engine.connect()
for i, row in raw_df.iterrows():
    print(f"Will look for product with name {row['name']}")
    product_id = product_df.loc[product_df['name'] == row['name'], 'id'].values[0]
    if stock_df.loc[stock_df['product_id'] == product_id, 'quantity'].values[0] != row['quantity']:
        print(f"Will update product with id {product_id}, with name {row['name']} to quantity {row['quantity']}")
        # insert_values = {'product_id': product_id, 'quantity': row['quantity']}
        stmt = stock_tbl.update().where(stock_tbl.c.product_id == product_id).values({'quantity': row['quantity']})
        con.execute(stmt)
    else:
        print(f"Quantity of {product_id}:{row['name']} hasn't changed so will skip it")
