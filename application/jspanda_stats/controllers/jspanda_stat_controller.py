import os
from flask import current_app
from application.jspanda_orders.models.jspanda_order import JspandaOrder, db
import datetime
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from application.utils.utils import to_yyyymmdd
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateField, IntegerField, FloatField, TextAreaField
from application.utils.utils import to_yyyymmdd


class JspandaStatForm(FlaskForm):
    start = DateField("Start date", format='%Y%m%d', render_kw={"class": "form-control"})
    end = DateField("End date", format='%Y%m%d', render_kw={"class": "form-control"})
    submit = SubmitField("Submit", render_kw={"class": "btn btn-lg btn-dark"})


class JspandaStatController:
    def __init__(self):
        self.name = "jspanda statistics"

    def jspanda_stats_home(self):
        form = JspandaStatForm()
        if form.validate_on_submit():
            return self.product_sales_stats(to_yyyymmdd(form.start.data), to_yyyymmdd(form.end.data))
        return render_template("jspanda_stats_home.html", title="Jspanda Statistics", form=form)

    def product_sales_stats(self, from_date_str, to_date_str):
        # from_date = datetime.datetime.strptime(from_date_str, '%Y%m%d')
        # to_date = datetime.datetime.strptime(to_date_str, '%Y%m%d')
        query = f"""select * from jspanda_orders where date between {from_date_str} and {to_date_str}"""
        df = pd.read_sql(query, db.engine)
        # plt.figure(figsize=(40, 10))
        g = sns.catplot(x='name', y='total_cost', data=df, kind='bar', height=5, aspect=3)
        g.fig.suptitle('Products by total cost')
        g.set(xlabel='product name', ylabel='total cost')
        plt.xticks(rotation=90)
        # grp_df = df.groupby('name').sum()[['total_cost']]
        # grp_df.sort_values('total_cost', ascending=False, inplace=True)
        # target_df = grp_df[:20]
        # plt.figure()
        # plt.barh(np.arange(len(target_df)), target_df['total_cost'].values, align='center', alpha=0.5)
        # plt.yticks(np.arange(len(target_df)), target_df.index)
        # plt.xlabel('Total cost')
        # plt.title(f'Product sales from {from_date_str} to {to_date_str}')
        # plt.tight_layout()
        plt.savefig(os.path.join(current_app.config['JSPANDA_STATS_FOLDER'], f'product_sales_{from_date_str}_to_{to_date_str}.svg'))
        return render_template("jspanda_stats.html", title="Product sales", graph_filename=f'product_sales_{from_date_str}_to_{to_date_str}.svg')
