import datetime
from application.jspanda_orders.models.jspanda_order import JspandaOrder, db
from application.admin.models.shipment_weight import ShipmentWeight
from application.admin.models.jpost_spending import JpostSpending
import logging
import numpy as np
import pandas as pd
from flask import redirect, url_for
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, FloatField, TextAreaField
from collections import namedtuple
import re


class JspandaOrderForm(FlaskForm):
    date = DateField("Date", render_kw={"class": "form-control"})
    name = StringField("Product name", render_kw={"class": "form-control"})
    quantity = IntegerField("Quantity", render_kw={"class": "form-control", "pattern": "[0-9]*"})
    price = FloatField("Cost per unit", render_kw={"class": "form-control"})
    selling_price_per_unit = FloatField("Price for sale", render_kw={"class": "form-control"})
    ordered_by = StringField("Ordered by", render_kw={"class": "form-control"})
    extra_notes = TextAreaField("Extra notes", render_kw={"class": "form-control"})
    submit = SubmitField("Submit", render_kw={"class": "btn btn-lg btn-dark"})


class JspandaOrderController:
    def __init__(self):
        self.name = "jspanda_controller"
        self.usdjpy_rate = 100

    def get_jspanda_na_prodaju_orders(self):
        jspanda_orders_df = pd.read_sql(JspandaOrder.query.statement, JspandaOrder.query.session.bind)
        jspanda_orders_df["ordered_by"]=jspanda_orders_df["ordered_by"].fillna("").apply(str)
        jspanda_orders_df['is_for_jspanda_stock'] = jspanda_orders_df['ordered_by'].map(lambda x: True if re.search("na prodaju", x) else False)
        jspanda_stock_df = jspanda_orders_df.loc[jspanda_orders_df['is_for_jspanda_stock']].copy()
        jspanda_stock_pvt_df = pd.pivot_table(jspanda_stock_df, index='date', values=['total_cost', 'order_sum', 'is_paid'], aggfunc={'total_cost': 'sum', 'order_sum': 'sum', 'is_paid': 'mean'})
        return jspanda_stock_pvt_df

    def get_jspanda_not_na_prodaju_orders(self):
        jspanda_orders_df = pd.read_sql(JspandaOrder.query.statement, JspandaOrder.query.session.bind)
        jspanda_orders_df["ordered_by"] = jspanda_orders_df["ordered_by"].fillna("").apply(str)
        jspanda_orders_df['is_for_jspanda_stock'] = jspanda_orders_df['ordered_by'].map(lambda x: True if re.search("na prodaju", x) else False)
        jspanda_stock_df = jspanda_orders_df.loc[np.logical_not(jspanda_orders_df['is_for_jspanda_stock'])].copy()
        jspanda_stock_pvt_df = pd.pivot_table(jspanda_stock_df, index='date', values=['total_cost', 'order_sum', 'is_paid'], aggfunc={'total_cost': 'sum', 'order_sum': 'sum', 'is_paid': 'mean'})
        return jspanda_stock_pvt_df

    def get_jspanda_orders_shipments_merged(self):
        df = pd.read_sql(JspandaOrder.query.statement, JspandaOrder.query.session.bind)
        orders_df = pd.pivot_table(df, index='date', values=['total_cost', 'order_sum', 'is_paid'], aggfunc={'total_cost': 'sum', 'order_sum': 'sum', 'is_paid': 'mean'})
        na_prodaju_orders_df = self.get_jspanda_na_prodaju_orders()
        orders_df = pd.merge(left=orders_df, right=na_prodaju_orders_df, left_index=True, right_index=True, how="left", suffixes=('', '_na_prodaju'))

        ne_na_prodaju_orders_df = self.get_jspanda_not_na_prodaju_orders()
        orders_df = pd.merge(left=orders_df, right=ne_na_prodaju_orders_df, left_index=True, right_index=True, how="left", suffixes=('', '_ne_na_prodaju'))

        shipment_weights_df = pd.read_sql(ShipmentWeight.query.statement, ShipmentWeight.query.session.bind)
        shipment_weights_df['total_shipment_spending_usd'] = shipment_weights_df['amount'] / self.usdjpy_rate
        shipment_weights_by_date_df = shipment_weights_df.groupby("order_date").sum()[['total_shipment_spending_usd']]

        jpost_df = pd.read_sql(JpostSpending.query.statement, JpostSpending.query.session.bind)
        jpost_by_date_df = jpost_df.groupby('order_date').sum()[['amount']]
        jpost_by_date_df['jpost_amount_usd'] = jpost_by_date_df['amount'] / self.usdjpy_rate

        orders_mrg_df = pd.merge(left=orders_df, right=shipment_weights_by_date_df, left_index=True, right_index=True, how="left")
        orders_shipment_mrg_df = pd.merge(left=orders_mrg_df, right=jpost_by_date_df, left_index=True, right_index=True, how="left")
        orders_shipment_mrg_df.fillna(0, inplace=True)
        orders_shipment_mrg_df['profit'] = orders_shipment_mrg_df['order_sum'] - orders_shipment_mrg_df['total_cost'] - orders_shipment_mrg_df['total_shipment_spending_usd'] - orders_shipment_mrg_df['jpost_amount_usd']
        orders_shipment_mrg_df = orders_shipment_mrg_df.sort_index(ascending=False)

        pending_product_cost = orders_shipment_mrg_df.loc[orders_shipment_mrg_df['is_paid'] != 1, 'total_cost'].sum()
        pending_shipment_cost = orders_shipment_mrg_df.loc[orders_shipment_mrg_df['is_paid'] != 1, 'total_shipment_spending_usd'].sum()
        pending_yubin_cost = orders_shipment_mrg_df.loc[orders_shipment_mrg_df['is_paid'] != 1, 'jpost_amount_usd'].sum()
        pending_total_cost = pending_product_cost + pending_shipment_cost + pending_yubin_cost

        total_product_cost = orders_shipment_mrg_df['total_cost'].sum()
        total_shipment_cost = orders_shipment_mrg_df['total_shipment_spending_usd'].sum()
        total_yubin_cost = orders_shipment_mrg_df['jpost_amount_usd'].sum()
        total_cost = total_product_cost + total_shipment_cost + total_yubin_cost
        total_revenue = orders_shipment_mrg_df['order_sum'].sum()
        total_profit = orders_shipment_mrg_df['profit'].sum()

        start_date = orders_shipment_mrg_df.index.min()
        end_date = orders_shipment_mrg_df.index.max()

        ret = namedtuple('ret', ['orders_shipment_mrg_df', 'pending_product_cost', 'pending_shipment_cost', 'pending_yubin_cost', 'pending_total_cost', 'total_product_cost', 'total_shipment_cost', 'total_yubin_cost', 'total_cost', 'total_revenue', 'total_profit', 'start_date', 'end_date'])
        return ret(orders_shipment_mrg_df, pending_product_cost, pending_shipment_cost, pending_yubin_cost, pending_total_cost, total_product_cost, total_shipment_cost, total_yubin_cost, total_cost, total_revenue, total_profit, start_date, end_date)

    def jspanda_orders_home(self):
        orders_shipments_merged = self.get_jspanda_orders_shipments_merged()
        return render_template("jspanda_orders_home.html", title="Jspanda home", adate=datetime.date.today(),
                               pending_product_cost=orders_shipments_merged.pending_product_cost,
                               pending_shipment_cost=orders_shipments_merged.pending_shipment_cost,
                               pending_yubin_cost=orders_shipments_merged.pending_yubin_cost,
                               pending_total_cost=orders_shipments_merged.pending_total_cost,
                               total_product_cost=orders_shipments_merged.total_product_cost,
                               total_shipment_cost=orders_shipments_merged.total_shipment_cost,
                               total_yubin_cost=orders_shipments_merged.total_yubin_cost,
                               total_cost=orders_shipments_merged.total_cost,
                               total_revenue=orders_shipments_merged.total_revenue,
                               total_profit=orders_shipments_merged.total_profit,
                               start_date=orders_shipments_merged.start_date,
                               end_date=orders_shipments_merged.end_date)

    def show_jspanda_orders(self):
        orders_shipments_merged = self.get_jspanda_orders_shipments_merged()
        orders_shipment_mrg_df = orders_shipments_merged.orders_shipment_mrg_df
        orders_shipment_mrg_df['profit_na_prodaju'] = orders_shipment_mrg_df['order_sum_na_prodaju'] - orders_shipment_mrg_df['total_cost_na_prodaju']
        orders_shipment_mrg_df['profit_ne_na_prodaju'] = orders_shipment_mrg_df['order_sum_ne_na_prodaju'] - orders_shipment_mrg_df['total_cost_ne_na_prodaju']
        orders_shipment_mrg_df['na_prodaju_and_ne_na_prodaju_total_profit'] = orders_shipment_mrg_df['profit_na_prodaju'] + orders_shipment_mrg_df['profit_ne_na_prodaju']
        orders_shipment_mrg_df['na_prodaju_profit_weight'] = orders_shipment_mrg_df['profit_na_prodaju'] / orders_shipment_mrg_df['na_prodaju_and_ne_na_prodaju_total_profit']
        orders_shipment_mrg_df['ne_na_prodaju_profit_weight'] = orders_shipment_mrg_df['profit_ne_na_prodaju'] / orders_shipment_mrg_df['na_prodaju_and_ne_na_prodaju_total_profit']
        orders_shipment_mrg_df['profit_na_prodaju_adjusted'] = orders_shipment_mrg_df['na_prodaju_profit_weight'] * orders_shipment_mrg_df['profit']
        orders_shipment_mrg_df['profit_ne_na_prodaju_adjusted'] = orders_shipment_mrg_df['ne_na_prodaju_profit_weight'] * orders_shipment_mrg_df['profit']
        return render_template("jspanda_orders.html", title="Jspanda Orders",
                               orders_shipment_mrg_df=orders_shipments_merged.orders_shipment_mrg_df,
                               adate=datetime.date.today(),
                               pending_product_cost=orders_shipments_merged.pending_product_cost,
                               pending_shipment_cost=orders_shipments_merged.pending_shipment_cost,
                               pending_yubin_cost=orders_shipments_merged.pending_yubin_cost,
                               pending_total_cost=orders_shipments_merged.pending_total_cost,
                               total_product_cost=orders_shipments_merged.total_product_cost,
                               total_shipment_cost=orders_shipments_merged.total_shipment_cost,
                               total_yubin_cost=orders_shipments_merged.total_yubin_cost,
                               total_cost=orders_shipments_merged.total_cost,
                               total_revenue=orders_shipments_merged.total_revenue,
                               total_profit=orders_shipments_merged.total_profit,
                               start_date=orders_shipments_merged.start_date,
                               end_date=orders_shipments_merged.end_date)

    def show_jspanda_pod_zakaz_orders(self):
        orders_shipments_merged = self.get_jspanda_orders_shipments_merged()
        orders_shipment_mrg_df = orders_shipments_merged.orders_shipment_mrg_df
        orders_shipment_mrg_df['profit_na_prodaju'] = orders_shipment_mrg_df['order_sum_na_prodaju'] - orders_shipment_mrg_df['total_cost_na_prodaju']
        orders_shipment_mrg_df['profit_ne_na_prodaju'] = orders_shipment_mrg_df['order_sum_ne_na_prodaju'] - orders_shipment_mrg_df['total_cost_ne_na_prodaju']
        orders_shipment_mrg_df['na_prodaju_and_ne_na_prodaju_total_profit'] = orders_shipment_mrg_df['profit_na_prodaju'] + orders_shipment_mrg_df['profit_ne_na_prodaju']
        orders_shipment_mrg_df['na_prodaju_profit_weight'] = orders_shipment_mrg_df['profit_na_prodaju'] / orders_shipment_mrg_df['na_prodaju_and_ne_na_prodaju_total_profit']
        orders_shipment_mrg_df['ne_na_prodaju_profit_weight'] = orders_shipment_mrg_df['profit_ne_na_prodaju'] / orders_shipment_mrg_df['na_prodaju_and_ne_na_prodaju_total_profit']
        orders_shipment_mrg_df['profit_na_prodaju_adjusted'] = orders_shipment_mrg_df['na_prodaju_profit_weight'] * orders_shipment_mrg_df['profit']
        orders_shipment_mrg_df['profit_ne_na_prodaju_adjusted'] = orders_shipment_mrg_df['ne_na_prodaju_profit_weight'] * orders_shipment_mrg_df['profit']
        pending_product_cost = orders_shipment_mrg_df.loc[orders_shipment_mrg_df['is_paid'] != 1, 'total_cost_ne_na_prodaju'].sum()
        return render_template("jspanda_orders_pod_zakaz.html", title="Под заказ", orders_shipment_mrg_df=orders_shipments_merged.orders_shipment_mrg_df, pending_product_cost=pending_product_cost)

    def show_jspanda_na_prodaju_orders(self):
        orders_shipments_merged = self.get_jspanda_orders_shipments_merged()
        orders_shipment_mrg_df = orders_shipments_merged.orders_shipment_mrg_df
        orders_shipment_mrg_df['profit_na_prodaju'] = orders_shipment_mrg_df['order_sum_na_prodaju'] - orders_shipment_mrg_df['total_cost_na_prodaju']
        orders_shipment_mrg_df['profit_ne_na_prodaju'] = orders_shipment_mrg_df['order_sum_ne_na_prodaju'] - orders_shipment_mrg_df['total_cost_ne_na_prodaju']
        orders_shipment_mrg_df['na_prodaju_and_ne_na_prodaju_total_profit'] = orders_shipment_mrg_df['profit_na_prodaju'] + orders_shipment_mrg_df['profit_ne_na_prodaju']
        orders_shipment_mrg_df['na_prodaju_profit_weight'] = orders_shipment_mrg_df['profit_na_prodaju'] / orders_shipment_mrg_df['na_prodaju_and_ne_na_prodaju_total_profit']
        orders_shipment_mrg_df['ne_na_prodaju_profit_weight'] = orders_shipment_mrg_df['profit_ne_na_prodaju'] / orders_shipment_mrg_df['na_prodaju_and_ne_na_prodaju_total_profit']
        orders_shipment_mrg_df['profit_na_prodaju_adjusted'] = orders_shipment_mrg_df['na_prodaju_profit_weight'] * orders_shipment_mrg_df['profit']
        orders_shipment_mrg_df['profit_ne_na_prodaju_adjusted'] = orders_shipment_mrg_df['ne_na_prodaju_profit_weight'] * orders_shipment_mrg_df['profit']
        pending_product_cost = orders_shipment_mrg_df.loc[orders_shipment_mrg_df['is_paid'] != 1, 'total_cost_na_prodaju'].sum()
        return render_template("na_prodaju/jspanda_orders_na_prodaju.html", title="На продажу по дням отправки", orders_shipment_mrg_df=orders_shipments_merged.orders_shipment_mrg_df, pending_product_cost=pending_product_cost)

    def show_jspanda_orders_unsold_na_prodaju(self):
        """

        :return:
        """
        query = JspandaOrder.query.filter(JspandaOrder.is_na_prodaju == True, JspandaOrder.is_paid == False)
        unsold_na_prodaju_df = pd.read_sql(query.statement, query.session.bind)
        unsold_na_prodaju_df['profit'] = unsold_na_prodaju_df['order_sum'] - unsold_na_prodaju_df['total_cost']
        pending_cost = unsold_na_prodaju_df['total_cost'].sum()
        pending_revenue = unsold_na_prodaju_df['order_sum'].sum()
        pending_profit = pending_revenue - pending_cost
        return render_template("na_prodaju/unsold_na_prodaju.html", unsold_na_prodaju_df=unsold_na_prodaju_df, pending_cost=pending_cost, pending_revenue=pending_revenue, pending_profit=pending_profit)

    def show_jspanda_orders_by_date_na_prodaju(self, adate):
        query = JspandaOrder.query.filter(JspandaOrder.date == adate, JspandaOrder.is_na_prodaju == True)
        orders_df = pd.read_sql(query.statement, query.session.bind)
        orders_df['profit'] = orders_df['total_cost']
        total_cost = orders_df['total_cost'].sum()
        total_revenue = orders_df['order_sum'].sum()
        total_profit = total_revenue - total_cost
        return render_template("na_prodaju/jspanda_orders_single_date_na_prodaju.html", title=f"Товары на продажу отправленные  {adate}", adate=adate, orders_df=orders_df, total_cost=total_cost, total_revenue=total_revenue, total_profit=total_profit)

    def show_jspanda_orders_all_na_prodaju(self):
        query = JspandaOrder.query.filter(JspandaOrder.is_na_prodaju == True)
        na_prodaju_df = pd.read_sql(query.statement, query.session.bind)
        na_prodaju_df['profit'] = na_prodaju_df['order_sum'] - na_prodaju_df['total_cost']
        total_cost = na_prodaju_df['total_cost'].sum()
        total_revenue = na_prodaju_df['order_sum'].sum()
        total_profit = total_revenue - total_cost
        return render_template("na_prodaju/all_na_prodaju.html", na_prodaju_df=na_prodaju_df, total_cost=total_cost, total_revenue=total_revenue, total_profit=total_profit)

    def show_jspanda_monthly_profit(self):
        df = pd.read_sql(JspandaOrder.query.statement, JspandaOrder.query.session.bind)
        # orders_cost_df = df.groupby('date').sum()[['total_cost', 'order_sum']]
        # orders_is_paid_df = df.groupby('date').mean()[['is_paid']]
        orders_df = pd.pivot_table(df, index='date', values=['total_cost', 'order_sum', 'is_paid'], aggfunc={'total_cost': 'sum', 'order_sum': 'sum', 'is_paid': 'mean'})
        shipment_weights_df = pd.read_sql(ShipmentWeight.query.statement, ShipmentWeight.query.session.bind)
        shipment_weights_df['total_shipment_spending_usd'] = shipment_weights_df['amount'] / self.usdjpy_rate
        shipment_weights_by_date_df = shipment_weights_df.groupby("order_date").sum()[['total_shipment_spending_usd']]

        jpost_df = pd.read_sql(JpostSpending.query.statement, JpostSpending.query.session.bind)
        jpost_by_date_df = jpost_df.groupby('order_date').sum()[['amount']]
        jpost_by_date_df['jpost_amount_usd'] = jpost_by_date_df['amount'] / self.usdjpy_rate

        orders_mrg_df = pd.merge(left=orders_df, right=shipment_weights_by_date_df, left_index=True, right_index=True, how="left")
        orders_shipment_mrg_df = pd.merge(left=orders_mrg_df, right=jpost_by_date_df, left_index=True, right_index=True, how="left")
        orders_shipment_mrg_df.fillna(0, inplace=True)
        orders_shipment_mrg_df['profit'] = orders_shipment_mrg_df['order_sum'] - orders_shipment_mrg_df['total_cost'] - orders_shipment_mrg_df['total_shipment_spending_usd'] - orders_shipment_mrg_df['jpost_amount_usd']
        orders_shipment_mrg_df = orders_shipment_mrg_df.sort_index(ascending=False)
        orders_shipment_mrg_df['year_month'] = orders_shipment_mrg_df.index.map(lambda x: datetime.date(x.year, x.month, 1))
        monthly_jspanda_orders_df = orders_shipment_mrg_df.groupby('year_month').sum()
        pending_product_cost = orders_shipment_mrg_df.loc[orders_shipment_mrg_df['is_paid'] != 1, 'total_cost'].sum()
        pending_shipment_cost = orders_shipment_mrg_df.loc[orders_shipment_mrg_df['is_paid'] != 1, 'total_shipment_spending_usd'].sum()
        pending_yubin_cost = orders_shipment_mrg_df.loc[orders_shipment_mrg_df['is_paid'] != 1, 'jpost_amount_usd'].sum()
        pending_total_cost = pending_product_cost + pending_shipment_cost + pending_yubin_cost
        return render_template("jspanda_monthly_summary.html", title="Jspanda orders", monthly_jspanda_orders_df=monthly_jspanda_orders_df, pending_product_cost=pending_product_cost, pending_shipment_cost=pending_shipment_cost, pending_yubin_cost=pending_yubin_cost, pending_total_cost=pending_total_cost)

    def show_jspanda_orders_by_date(self, adate):
        records = JspandaOrder.query.filter(JspandaOrder.date == adate).order_by(JspandaOrder.modified_time.desc()).all()
        orders_df = pd.read_sql(JspandaOrder.query.filter(JspandaOrder.date == adate).statement, JspandaOrder.query.filter(JspandaOrder.date == adate).session.bind)
        shipment_weights_df = pd.read_sql(ShipmentWeight.query.filter(ShipmentWeight.order_date == adate).statement, ShipmentWeight.query.filter(ShipmentWeight.order_date == adate).session.bind)
        jpost_df = pd.read_sql(JpostSpending.query.filter(JpostSpending.order_date == adate).statement, JpostSpending.query.filter(JpostSpending.order_date == adate).session.bind)
        total_cost = orders_df['total_cost'].sum()
        total_order_sum = orders_df['order_sum'].sum()
        total_shipment_spending = shipment_weights_df['amount'].sum() / self.usdjpy_rate
        total_yubin_spending = jpost_df['amount'].sum() / self.usdjpy_rate
        profit = total_order_sum - total_cost - total_shipment_spending - total_yubin_spending
        return render_template("jspanda_orders_single_date.html", title=f"Jspanda order as of {adate}", adate=adate, records=records, total_cost=total_cost, total_order_sum=total_order_sum, total_shipment_spending=total_shipment_spending, total_yubin_spending=total_yubin_spending, profit=profit)

    def add_jspanda_order(self, adate):
        form = JspandaOrderForm()
        if form.validate_on_submit():
            total_cost = form.price.data * form.quantity.data
            order_sum = form.selling_price_per_unit.data * form.quantity.data
            new_record = JspandaOrder(date=form.date.data, name=form.name.data, quantity=form.quantity.data, price=form.price.data, selling_price_per_unit=form.selling_price_per_unit.data,
                                      ordered_by=form.ordered_by.data,
                                      extra_notes=form.extra_notes.data,
                                      total_cost=total_cost,
                                      order_sum=order_sum,
                                      is_paid=False,
                                      is_received=False,
                                      added_time=datetime.datetime.now(),
                                      modified_time=datetime.datetime.now())
            db.session.add(new_record)
            db.session.commit()
            flash(f"Added {new_record} successfully", "success")
            # return self.show_jspanda_orders_by_date(form.date.data)
            return redirect(f"/jspanda_orders_by_date/{form.date.data}")
        form.date.data = datetime.datetime.strptime(adate, '%Y-%m-%d')
        return render_template("add_jspanda_order.html", title="Add jspanda order", form=form)

    def edit_jspanda_order(self, id):
        record = JspandaOrder.query.get(id)
        form = JspandaOrderForm()
        if form.validate_on_submit():
            record.date = form.date.data
            record.name = form.name.data
            record.quantity = form.quantity.data
            record.price = form.price.data
            record.selling_price_per_unit = form.selling_price_per_unit.data
            record.ordered_by = form.ordered_by.data
            record.extra_notes = form.extra_notes.data
            record.total_cost = record.price * record.quantity
            record.order_sum = record.selling_price_per_unit * record.quantity
            record.modified_time = datetime.datetime.now()
            db.session.commit()
            flash(f"Edited jspanda order {id}", "success")
            # return self.show_jspanda_orders_by_date(record.date)
            return redirect(f"/jspanda_orders_by_date/{record.date}")
        form.date.data = record.date
        form.name.data = record.name
        form.quantity.data = record.quantity
        form.price.data = record.price
        form.selling_price_per_unit.data = record.selling_price_per_unit
        form.ordered_by.data = record.ordered_by
        form.extra_notes.data = record.extra_notes
        return render_template("edit_jspanda_order.html", form=form)

    def remove_jspanda_order(self, id):
        record = JspandaOrder.query.get(id)
        adate = record.date
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed {id}", "success")
        # return self.show_jspanda_orders_by_date(adate)
        return redirect(f"/jspanda_orders_by_date/{adate}")

    def mark_as_paid_or_nonpaid(self, id, from_page=""):
        record = JspandaOrder.query.get(id)
        if record.is_paid == True:
            record.is_paid = False
        else:
            record.is_paid = True
        record.modified_time = datetime.datetime.now()
        db.session.commit()
        flash(f"Marked {record.id},{record.name} is_paid to {record.is_paid} ", "success")
        if from_page == 'jspanda_orders_by_date_na_prodaju':
            logging.info(f"from page is : {from_page}")
            return redirect(f"/{from_page}/{record.date}")
        if from_page == 'all_na_prodaju':
            return redirect(url_for('jspanda_orders_bp.jspanda_orders_all_na_prodaju'))
        if from_page=='unsold_na_prodaju':
            return redirect(url_for('jspanda_orders_bp.jspanda_orders_unsold_na_prodaju'))
        return redirect(f"/jspanda_orders_by_date/{record.date}")

    def mark_as_paid_or_nonpaid_by_date(self, adate_str):
        adate = datetime.datetime.strptime(adate_str, '%Y-%m-%d')
        records = JspandaOrder.query.filter(JspandaOrder.date == adate).all()
        df = pd.read_sql(JspandaOrder.query.filter(JspandaOrder.date == adate).statement, JspandaOrder.query.filter(JspandaOrder.date == adate).session.bind)
        if df['is_paid'].mean() != 1:
            for record in records:
                record.is_paid = True
                db.session.commit()
            flash(f"Closed {adate}", "success")
            return redirect("/jspanda_orders")
        else:
            for record in records:
                record.is_paid = False
                db.session.commit()
            flash(f"Reopened {adate}", "success")
            return redirect("/jspanda_orders")

    def mark_as_recived_or_nonreceived(self, id):
        record = JspandaOrder.query.get(id)
        if record.is_received:
            record.is_received = False
        else:
            record.is_received = True
        record.modified_time = datetime.datetime.now()
        db.session.commit()
        flash(f"Marked {record.id},{record.name} is_received to {record.is_received}", "success")
        # return self.show_jspanda_orders_by_date(record.date)
        return redirect(f"/jspanda_orders_by_date/{record.date}")

    def mark_as_received_by_date(self, adate_str):
        adate = datetime.datetime.strptime(adate_str, '%Y-%m-%d')
        records = JspandaOrder.query.filter(JspandaOrder.date == adate).all()
        for record in records:
            record.is_received = True
            db.session.commit()
        flash(f"Marked all items for  {adate} as arrived in Tashkent", "success")
        return redirect(f"/jspanda_orders_by_date/{adate_str}")

    def mark_as_yubin_received_or_nonreceived(self, id):
        record = JspandaOrder.query.get(id)
        if record.is_yubin_received:
            record.is_yubin_received = False
        else:
            record.is_yubin_received = True
        record.modified_time = datetime.datetime.now()
        db.session.commit()
        flash(f"Marked {id} as yubin received or nonreceived", 'success')
        return redirect(f"/jspanda_orders_by_date/{record.date}")
