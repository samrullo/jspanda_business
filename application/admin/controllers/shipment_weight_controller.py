import datetime

from application.admin.models.shipment_usdjpy_rate import ShipmentUSDJPYRate
from application.admin.models.shipment_weight import ShipmentWeight, ShipmentPrice, ShipmentPriceUSD, db
import logging
import pandas as pd
import numpy as np
from flask import current_app
from flask import flash
from flask import render_template
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, IntegerField, DateField, FloatField
from application.utils.utils import to_yyyymmdd


class ShipmentWeightForm(FlaskForm):
    date = DateField("Date", render_kw={"class": "form-control"})
    order_date = DateField("Order Date", render_kw={"class": "form-control"})
    to_whom = StringField("To whom", render_kw={"class": "form-control"})
    weight = FloatField("Weight", render_kw={"class": "form-control", "pattern": "[0-9]+([\.,][0-9]+)?", "step": "0.01"})
    # pattern="[0-9]+([\.,][0-9]+)?" step="0.01"
    #
    submit = SubmitField("Submit", render_kw={"class": "btn bnt-lg btn-dark"})


def get_shipment_price_usd(shipment_date: datetime.date):
    shipment_usd_prices = ShipmentPriceUSD.query.filter(ShipmentPriceUSD.start <= shipment_date).filter(ShipmentPriceUSD.end >= shipment_date).all()
    shipment_usd_prices = sorted(shipment_usd_prices, key=lambda record: record.start)
    shipment_usd_price = shipment_usd_prices[-1]
    return shipment_usd_price.price


class ShipmentWeightController:
    def __init__(self):
        shipment_prices = ShipmentPrice.query.filter(ShipmentPrice.end == None).all()
        current_app.logger.info(f"below are retrieved shipment prices : {shipment_prices}")
        if len(shipment_prices) > 0:
            self.shipment_per_kg_price = shipment_prices[0].price
        else:
            self.shipment_per_kg_price = 2000

    def show_pending_shipment_weights(self):
        records = ShipmentWeight.query.filter(ShipmentWeight.is_paid == False).order_by(ShipmentWeight.date.desc()).all()
        df = pd.read_sql(ShipmentWeight.query.statement, ShipmentWeight.query.session.bind)
        total_weight = df.loc[np.logical_not(df.is_paid), 'weight'].sum()
        total_amount = df.loc[np.logical_not(df.is_paid), 'amount'].sum()
        total_amount_usd = df.loc[np.logical_not(df.is_paid), 'amount_usd'].sum()
        return render_template("shipment_weight/shipment_weight_main.html", records=records, total_amount=total_amount, total_amount_usd=total_amount_usd, total_weight=total_weight, title="Pending Shipment weights")

    def show_all_shipment_weights(self):
        records = ShipmentWeight.query.order_by(ShipmentWeight.date.desc()).all()
        df = pd.read_sql(ShipmentWeight.query.statement, ShipmentWeight.query.session.bind)
        total_weight = df['weight'].sum()
        total_amount = df['amount'].sum()
        return render_template("shipment_weight/view_all_shipment_weight.html", records=records, total_amount=total_amount, total_weight=total_weight, title="All Shipment weights")

    def show_shipment_weights_by_date(self):
        df = pd.read_sql(ShipmentWeight.query.statement, ShipmentWeight.query.session.bind)
        shipments_df = df.groupby('date').sum()[['weight', 'amount']]
        shipments_df.sort_index(ascending=False, inplace=True)
        return render_template("shipment_weight/show_shipment_weights_by_date.html", shipments_df=shipments_df, title="Shipment weights by date")

    def add_shipment_weight(self):
        form = ShipmentWeightForm()
        if form.validate_on_submit():
            date = form.date.data
            order_date = form.order_date.data
            to_whom = form.to_whom.data
            weight = form.weight.data
            shipment_per_kg_price_usd = get_shipment_price_usd(date)
            amount_usd = weight * shipment_per_kg_price_usd
            shipment_usdjpy_rate = get_shipment_usdjpy_rate(date)
            amount = amount_usd * shipment_usdjpy_rate
            new_record = ShipmentWeight(date=date, order_date=order_date, to_whom=to_whom, weight=weight, amount_usd=amount_usd, amount=amount, is_paid=False)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Successfully added {date}, {weight} kg, {amount_usd} usd, {amount} jpy", "success")
            # return self.show_pending_shipment_weights()
            return redirect("/admin/show_shipment_weight")
        form.date.data = datetime.date.today()
        form.order_date.data = datetime.date.today()
        form.to_whom.data = "Sabina"
        return render_template("shipment_weight/shipment_weight_add.html", form=form, title="Add shipment weight")

    def edit_shipment_weight(self, id):
        record = ShipmentWeight.query.get(id)
        form = ShipmentWeightForm()
        if form.validate_on_submit():
            record.date = form.date.data
            record.order_date = form.order_date.data
            record.to_whom = form.to_whom.data
            record.weight = form.weight.data
            shipment_per_kg_price_usd = get_shipment_price_usd(record.date)
            record.amount_usd = record.weight * shipment_per_kg_price_usd
            shipment_usdjpy_rate = get_shipment_usdjpy_rate(record.date)
            record.amount = record.amount_usd * shipment_usdjpy_rate
            db.session.commit()
            flash(f"Updated to {record.date},{record.to_whom},{record.weight},{record.amount_usd} usd, {record.amount} jpy", "success")
            return redirect("/admin/show_shipment_weight")
        form.date.data = record.date
        form.order_date.data = record.order_date
        form.to_whom.data = record.to_whom
        form.weight.data = record.weight
        return render_template("shipment_weight/shipment_weight_edit.html", form=form, title="Edit shipment spending")

    def remove_shipment_weight(self, id):
        record = ShipmentWeight.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed id {id}", "success")
        return redirect("/admin/show_shipment_weight")

    def mark_as_paid(self, id):
        record = ShipmentWeight.query.get(id)
        record.is_paid = True
        db.session.commit()
        flash(f"Marked {id} as paid", "success")
        return redirect("/admin/show_shipment_weight")


def get_shipment_usdjpy_rate(order_date: datetime.date):
    shipment_usdjpy_rates = ShipmentUSDJPYRate.query.filter(ShipmentUSDJPYRate.start <= order_date).filter(ShipmentUSDJPYRate.end >= order_date).all()
    shipment_usdjpy_rates = sorted(shipment_usdjpy_rates, key=lambda record: record.start)
    shipment_usdjpy_rate = shipment_usdjpy_rates[-1]
    return shipment_usdjpy_rate.fx_rate
