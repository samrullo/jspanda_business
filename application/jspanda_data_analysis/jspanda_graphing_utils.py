import matplotlib.pyplot as plt
import numpy as np
import os


def autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                f"{height:,.2f}",
                ha='center', va='bottom')


def set_matplotlib_text_font(font_size=8):
    """
    set text font size
    :return:
    """
    plt.rc('font', size=font_size)


def bar_plot_revenue_cost_side_by_side(grp_df, index_col_name, revenue_col_name, cost_col_name, title_prefix, working_folder, filename_prefix, figsize=(20, 10)):
    """

    :param grp_df:
    :param index_col_name:
    :param revenue_col_name:
    :param cost_col_name:
    :param title_prefix:
    :param working_folder:
    :param filename_prefix:
    :param figsize:
    :return:
    """
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
    print(f"finished {title_prefix} plotting")
