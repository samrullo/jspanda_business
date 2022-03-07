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
working_folder = r"C:\Users\amrul\Documents\japan_sweets_business\data_analysis\sales"


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


def make_year_month_cols(df, date_col):
    df["year"] = df[date_col].map(lambda _date: _date.year)
    df["month_no"] = df[date_col].map(lambda _date: _date.month)
    df["month"] = df[date_col].map(lambda _date: get_month_name_from_number()[_date.month])


jspanda_orders_df["year"] = jspanda_orders_df["date"].map(lambda _date: _date.year)
jspanda_orders_df["month_no"] = jspanda_orders_df["date"].map(lambda _date: _date.month)
jspanda_orders_df["month"] = jspanda_orders_df["date"].map(lambda _date: get_month_name_from_number()[_date.month])

by_year_month_df = jspanda_orders_df.groupby(["year", "month", "month_no"])[["total_cost", "order_sum"]].sum()
by_year_month_df = indices_to_columns(by_year_month_df)
by_year_month_df = by_year_month_df.sort_values(['year', 'month_no'])


def autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                f"{height:,.2f}",
                ha='center', va='bottom')


def set_matplotlib_text_size_to_small_font():
    SMALL_SIZE = 8
    plt.rc('font', size=SMALL_SIZE)


def bar_plot_revenue_cost_side_by_side(grp_df, index_col_name, revenue_col_name, cost_col_name, title_prefix, filename_prefix, figsize=(20, 10)):
    total_revenue = grp_df[revenue_col_name].sum()
    total_cost = grp_df[cost_col_name].sum()
    total_profit = total_revenue - total_cost
    fig, ax = plt.subplots(figsize=figsize)
    x_indices = np.arange(len(grp_df))
    bar_width = 0.4

    cost_rects = ax.bar(x_indices, grp_df[cost_col_name], bar_width)
    revenue_rects = ax.bar(x_indices + bar_width, grp_df[revenue_col_name], bar_width)
    autolabel(ax, cost_rects)
    autolabel(ax, revenue_rects)

    ax.set_ylabel("Dollar")
    ax.set_title(f"{title_prefix} - Total Revenue : {total_revenue:,.2f}, Total Cost : {total_cost:,.2f}, Profit : {total_profit:,.2f}")
    ax.set_xticks(x_indices + bar_width / 2)
    ax.set_xticklabels(grp_df[index_col_name])
    ax.legend((cost_rects[0], revenue_rects[0]), (cost_col_name, revenue_col_name))

    plt.show()
    plt.savefig(os.path.join(working_folder, f"{filename_prefix}_revenue_cost.jpg"), dpi=199)
    print(f"finished {one_year} plotting")


set_matplotlib_text_size_to_small_font()

for one_year in by_year_month_df["year"].unique():
    one_year_month_df = by_year_month_df[by_year_month_df.year == one_year]
    bar_plot_revenue_cost_side_by_side(one_year_month_df, "month", "order_sum", "total_cost", one_year, f"graph_{one_year}")

by_year_df = jspanda_orders_df.groupby(["year"])[["total_cost", "order_sum"]].sum()
by_year_df = indices_to_columns(by_year_df)
bar_plot_revenue_cost_side_by_side(by_year_df, "year", "order_sum", "total_cost", "all years", "all_years")
