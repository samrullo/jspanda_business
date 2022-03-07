import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Table
import os
import datetime
import sys
import logging
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]')


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


engine = create_engine('mysql://samrullo:18Rirezu@68.183.81.44/sql12359588?charset=utf8')

jspanda_orders_df = pd.read_sql("select * from jspanda_orders", engine)
print(f"jspanda_orders_df total records : {len(jspanda_orders_df)}")

jspanda_orders_df["year"] = jspanda_orders_df["date"].map(lambda _date: _date.year)
jspanda_orders_df["month_no"] = jspanda_orders_df["date"].map(lambda _date:_date.month)
jspanda_orders_df["month"] = jspanda_orders_df["date"].map(lambda _date: get_month_name_from_number()[_date.month])

by_year_month_df = jspanda_orders_df.groupby(["year", "month","month_no"])[["total_cost", "order_sum"]].sum()
by_year_month_df = indices_to_columns(by_year_month_df)

by_year_month_product_df = jspanda_orders_df.groupby(['year', 'month', 'month_no','name'])[["total_cost", "order_sum"]].sum()
by_year_month_product_df=indices_to_columns(by_year_month_product_df)
# by_year_month_product_df=jspanda_orders_df.pivot_table(index=["year","month","month_no","name"],columns=["total_cost","order_sum"],aggfunc="sum")

# g_total_cost = sns.catplot(x="month", y="total_cost", data=by_year_month_df, col="year", kind="bar", order=get_month_name_from_number().values())
# g_order_sum = sns.catplot(x="month", y="order_sum", data=by_year_month_df, col="year", kind="bar", order=get_month_name_from_number().values())
# g_order_sum.fig.suptitle("Total cost by month")
# plt.show()

# plt.figure()
# g = sns.catplot(x="name", data=jspanda_orders_df, kind="count")
# g.fig.suptitle("Count of sold products")
# plt.show()
