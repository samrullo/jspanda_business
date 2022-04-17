import pandas as pd
import os
import pathlib
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres@postgres:5432/jspanda")
folder = pathlib.Path("/app") / "postgres_data" / \
    "db_dumps" / "jspanda_db_dump_asof_20220415"
failed_tables = []
tables = []
for csv_file in folder.iterdir():
    tables.append(csv_file.stem)
print(f"extracted {len(tables)} tables : {tables}")

# make sure the order of category,product and stock
product_tables = ["category", "product", "stock"]
for tbl in product_tables:
    tables.remove(tbl)

tables = tables+product_tables

for tbl in tables:
    try:
        print(f"will load {tbl}")
        csv_file = folder/f"{tbl}.csv"
        df = pd.read_csv(csv_file)
        df = df.drop("id", axis=1)
        df.to_sql(tbl, engine, if_exists="append", index=False)
    except Exception as e:
        print(f"{tbl} loading failed : {e}")
        failed_tables.append(tbl)
        # print(f"will load with append")
        # df.to_sql(csv_file.stem, engine, if_exists="append")

print(f"tables that failed when attempting replace : {failed_tables}")
