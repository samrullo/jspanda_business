import datetime
from application.jspanda_orders.models.jspanda_order import JspandaOrder, db
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateField, IntegerField, FloatField, TextAreaField
from application.utils.utils import to_yyyymmdd


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

    def show_jspanda_orders(self):
        df = pd.read_sql(JspandaOrder.query.statement, JspandaOrder.query.session.bind)
        orders_df = df.groupby('date').sum()[['total_cost', 'order_sum']]
        orders_df['profit'] = orders_df['order_sum'] - orders_df['total_cost']
        orders_df=orders_df.sort_index(ascending=False)
        return render_template("jspanda_orders.html", title="Jspanda orders", orders_df=orders_df)

    def show_jspanda_orders_by_date(self, adate):
        records = JspandaOrder.query.filter(JspandaOrder.date == adate).all()
        return render_template("jspanda_orders_single_date.html", title=f"Jspanda order as of {adate}", records=records)

    def add_jspanda_order(self):
        form = JspandaOrderForm()
        if form.validate_on_submit():
            total_cost = form.price.data * form.quantity.data
            order_sum = form.selling_price_per_unit.data * form.quantity.data
            new_record = JspandaOrder(date=form.date.data, name=form.name.data, quantity=form.quantity.data, price=form.price.data, selling_price_per_unit=form.selling_price_per_unit.data,
                                      ordered_by=form.ordered_by.data,
                                      extra_notes=form.extra_notes.data,
                                      total_cost=total_cost,
                                      order_sum=order_sum,
                                      is_paid=False)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Added {new_record} successfully", "success")
            return self.show_jspanda_orders_by_date(form.date.data)
        return render_template("add_jspanda_order.html", title="Add jspanda order", form=form)

    def edit_jspanda_order(self, id):
        return

    def remove_jspanda_order(self, id):
        record = JspandaOrder.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed {id}", "success")
        return self.show_jspanda_orders()
