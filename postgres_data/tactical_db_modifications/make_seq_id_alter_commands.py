import pandas as pd
import os
import pathlib
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres@postgres:5432/jspanda")
_tables = engine.table_names()
alter_seq_commands = []
_tables_in_scope=[]
for tbl in _tables:
    query = f"select * from {tbl}"
    df = pd.read_sql(query, engine)
    if "id" in df.columns and len(df)>0:
        _tables_in_scope.append(tbl)
        _max_id = df["id"].max()
        cmd = f"ALTER SEQUENCE {tbl}_id_seq RESTART WITH {_max_id};"
        alter_seq_commands.append(cmd)
