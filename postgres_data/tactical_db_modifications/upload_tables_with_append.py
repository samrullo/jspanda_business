import pandas as pd
import os
import pathlib
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres@postgres:5432/jspanda")
folder = pathlib.Path("/app") / "postgres_data" / \
    "db_dumps" / "jspanda_db_dump_asof_20220415"
failed_tables = []

for csv_file in folder.iterdir():
    try:
        print(f"will load {csv_file}")
        df = pd.read_csv(csv_file)
        df = df.drop("id", axis=1)
        df.to_sql(csv_file.stem, engine, if_exists="append",index=False)
    except Exception as e:
        print(f"{csv_file.stem} loading failed : {e}")
        failed_tables.append(csv_file.stem)
        # print(f"will load with append")
        # df.to_sql(csv_file.stem, engine, if_exists="append")

print(f"tables that failed when attempting replace : {failed_tables}")