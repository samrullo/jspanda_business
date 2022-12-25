import click
from sqlalchemy import create_engine, MetaData, Table
from application.utils.utils import get_logger
from application.jspanda_orders_from_google.jspanda_orders_gspread import (
    GoogleSpreadsheetToDataframe,
)
from application.jspanda_orders_from_google.utils import validate_date
from datetime import datetime

logger = get_logger()

@click.command()
@click.option(
    "-u",
    "--db_uri",
    type=str,
    required=True,
    default="postgresql://postgres:postgres@postgres:5432/jspanda",
    help="database uri",
)
@click.option(
    "-g",
    "--gdoc_name",
    type=str,
    required=True,
    default="Japansweetproject_new.xlsx",
    help="google spreadsheet name",
)
@click.option(
    "--gdoc_sheet_name", type=str, required=True, help="google spreadsheet sheet name"
)
@click.option(
    "--adate",
    type=str,
    required=True,
    help="as of date in YYYYMMDD",
    callback=validate_date,
)
@click.option(
    "--fx_rate",
    type=int,
    required=True,
    default=125
)
def insert_jspanda_google_sheets(db_uri, gdoc_name, gdoc_sheet_name, adate,fx_rate):
    engine = create_engine(db_uri)
    g_docs_obj = GoogleSpreadsheetToDataframe()
    raw_df = g_docs_obj.get_worksheet_as_dataframe(gdoc_name, gdoc_sheet_name)
    if len(raw_df.columns) > 9:
        raw_df = raw_df.iloc[:, :9]

    if len(raw_df.columns) == 8:
        raw_df["extra_col"] = ""

    if len(raw_df.columns) == 7:
        raw_df["extra_col"] = ""
        raw_df["extra_col2"] = ""

    if len(raw_df.columns) == 6:
        raw_df["extra_col"] = ""
        raw_df["extra_col2"] = ""
        raw_df["extra_col3"] = ""

    jspanda_df = g_docs_obj.prepare_insertable_jspanda_orders_dataframe(raw_df, adate,utf8endcode=False,fx_rate=fx_rate)

    # next will insert jspanda_df records into database

    metadata = MetaData()
    jspanda_orders_tbl = Table(
        "jspanda_orders", metadata, autoload=True, autoload_with=engine
    )
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
        for col in ["is_received","is_yubin_received","is_na_prodaju"]:
            insert_values[col]=False
        _now=datetime.utcnow()
        insert_values["added_time"]=_now
        insert_values["modified_time"]=_now
        stmt = jspanda_orders_tbl.insert().values(insert_values)
        con.execute(stmt)


if __name__ == "__main__":
    insert_jspanda_google_sheets()
