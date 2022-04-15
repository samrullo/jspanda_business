import pandas as pd
import os
import pathlib
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres@postgres:5432/jspanda")
acc_file = pathlib.Path.cwd() / "postgres_data" / "db_dumps" / "account.csv"
acc_df = pd.read_csv(acc_file)
acc_df = acc_df.drop("id", axis=1)

acc_df.to_sql("account", engine, if_exists="replace")
