import datetime
from application.jspanda_orders.models.jspanda_order import JspandaOrder, db
from application.admin.models.shipment_weight import ShipmentWeight
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

    def jspanda_orders_home(self):
        return render_template("jspanda_orders_home.html", title="Jspanda home", adate=datetime.date.today())

    def show_jspanda_orders(self):
        df = pd.read_sql(JspandaOrder.query.statement, JspandaOrder.query.session.bind)
        orders_df = df.groupby('date').sum()[['total_cost', 'order_sum']]
        orders_df['profit'] = orders_df['order_sum'] - orders_df['total_cost']
        orders_df = orders_df.sort_index(ascending=False)
        return render_template("jspanda_orders.html", title="Jspanda orders", orders_df=orders_df)

    def show_jspanda_orders_by_date(self, adate):
        records = JspandaOrder.query.filter(JspandaOrder.date == adate).order_by(JspandaOrder.modified_time.desc()).all()
        return render_template("jspanda_orders_single_date.html", title=f"Jspanda order as of {adate}", adate=adate, records=records)

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
                                      added_time=datetime.datetime.now(),
                                      modified_time=datetime.datetime.now())
            db.session.add(new_record)
            db.session.commit()
            flash(f"Added {new_record} successfully", "success")
            return self.show_jspanda_orders_by_date(form.date.data)
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
            return self.show_jspanda_orders_by_date(record.date)
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
        return self.show_jspanda_orders_by_date(adate)

    def mark_as_paid_or_nonpaid(self, id):
        record = JspandaOrder.query.get(id)
        if record.is_paid == True:
            record.is_paid = False
        else:
            record.is_paid = True
        record.modified_time = datetime.datetime.now()
        db.session.commit()
        flash(f"Marked {record.id},{record.name} is_paid to {record.is_paid} ", "success")
        return self.show_jspanda_orders_by_date(record.date)