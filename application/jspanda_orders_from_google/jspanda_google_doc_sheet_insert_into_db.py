import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table
import os
import datetime
import sys
from application.utils.utils import get_logger
from application.jspanda_orders_from_google.jspanda_orders_gspread import GoogleSpreadsheetToDataframe

logger = get_logger()

engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))

gdoc_name = "Japansweetproject_new.xlsx"
gdoc_sheet_name = "Заказы 081119"

adate = datetime.date(2019, 11, 8)

g_docs_obj = GoogleSpreadsheetToDataframe()
raw_df = g_docs_obj.get_worksheet_as_dataframe(gdoc_name, gdoc_sheet_name)
jspanda_df = g_docs_obj.prepare_insertable_jspanda_orders_dataframe(raw_df, adate)

# next will insert jspanda_df records into database

metadata = MetaData()
jspanda_orders_tbl = Table("jspanda_orders", metadata, autoload=True, autoload_with=engine)
con = engine.connect()
for i, row in jspanda_df.iterrows():
    print(f"Will insert {i}, {row['name']}")
    insert_values = {}
    for key in jspanda_df.columns:
        insert_values[key] = row[key]
    stmt = jspanda_orders_tbl.insert().values(insert_values)
    con.execute(stmt)