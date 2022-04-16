import pandas as pd
import os
import pathlib
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres@postgres:5432/jspanda")
_tables = engine.table_names()
print(f"will make alter sequence commands for {len(_tables)} tables : {_tables}")
alter_seq_commands = []
_tables_in_scope = []
for tbl in _tables:
    query = f"select * from {tbl}"
    df = pd.read_sql(query, engine)
    if "id" in df.columns and len(df) > 0:
        _tables_in_scope.append(tbl)
        _max_id = df["id"].max()
        cmd = f"ALTER SEQUENCE {tbl}_id_seq RESTART WITH {_max_id};"
        alter_seq_commands.append(cmd)

print(f"out of {len(_tables)} {len(_tables_in_scope)} tables are in scope")
print(f"{set(_tables)-set(_tables_in_scope)} tables will be skipped")

# write commands into file
file = pathlib.Path("/app")/"postgres_data"/"db_dumps" / \
    "alter_seq_id_commands.sql"
if file.exists():
    os.remove(file)


with open(file, 'a') as fh:
    for cmd in alter_seq_commands:
        fh.write(f"{cmd}\n")
