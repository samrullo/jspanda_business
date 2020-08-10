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

gdoc_name = "Japansweetproject_new.xlsx"
gdoc_sheet_name = "Заказы 070820"

adate = datetime.date(2020, 8, 7)

g_docs_obj = GoogleSpreadsheetToDataframe()
raw_df = g_docs_obj.get_worksheet_as_dataframe(gdoc_name, gdoc_sheet_name)
if len(raw_df.columns) > 9:
    raw_df = raw_df.iloc[:, :9]

if len(raw_df.columns) == 8:
    raw_df['extra_col'] = ""

if len(raw_df.columns) == 7:
    raw_df['extra_col'] = ""
    raw_df['extra_col2'] = ""

jspanda_df = g_docs_obj.prepare_insertable_jspanda_orders_dataframe(raw_df, adate)

# next will insert jspanda_df records into database

metadata = MetaData()
jspanda_orders_tbl = Table("jspanda_orders", metadata, autoload=True, autoload_with=engine)
con = engine.connect()

# before inserting records we will remove existing records on a given date
stmt = jspanda_orders_tbl.delete().where(jspanda_orders_tbl.c.date == adate)
con.execute(stmt)
logger.info(f"Removed all jspanda order as of {adate}")

for i, row in jspanda_df.iterrows():
    print(f"Will insert {i}, {row['name']}")
    insert_values = {}
    for key in jspanda_df.columns:
        insert_values[key] = row[key]
    stmt = jspanda_orders_tbl.insert().values(insert_values)
    con.execute(stmt)
