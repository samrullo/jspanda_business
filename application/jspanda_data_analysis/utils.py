import datetime
import sys
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sqlalchemy import create_engine


def init_logging(level=logging.INFO):
    FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]'
    logging.basicConfig(level=level, format=FORMAT)


def get_jspanda_engine(is_local=True):
    if not is_local:
        return create_engine('mysql://samrullo:18Rirezu@68.183.81.44/sql12359588?charset=utf8')
    else:
        return create_engine('mysql://root:@localhost/sql12359588?charset=utf8')


def get_all_jspanda_orders(engine):
    jspanda_orders_df = pd.read_sql("select * from jspanda_orders", engine)
    print(f"jspanda_orders_df total records : {len(jspanda_orders_df)}")
    return jspanda_orders_df


def get_jspanda_orders_one_year(year, engine):
    jspanda_orders_df = pd.read_sql("select * from jspanda_orders", engine)
    jspanda_orders_df = make_year_month_cols(jspanda_orders_df, "date")
    jspanda_orders_df = jspanda_orders_df[jspanda_orders_df["year"] == year]
    print(f"jspanda_orders_df {year} total records : {len(jspanda_orders_df)}")
    return jspanda_orders_df


def indices_to_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.index.names:
        df[col] = df.index.get_level_values(col)
    df.index = range(len(df))
    return df


def get_month_name_from_number():
    return {1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec"}


def make_year_month_cols(df, date_col):
    df["year"] = df[date_col].map(lambda _date: _date.year)
    df["month_no"] = df[date_col].map(lambda _date: _date.month)
    df["month"] = df[date_col].map(lambda _date: get_month_name_from_number()[_date.month])
    return df
