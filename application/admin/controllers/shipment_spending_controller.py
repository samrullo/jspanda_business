import datetime
from flask import current_app
from application.admin.models.shipment_weight import ShipmentPrice
from application.admin.models.shipment_spending import ShipmentSpending, db
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, IntegerField, DateField, FloatField
from application.utils.utils import to_yyyymmdd


class ShipmentSpendingForm(FlaskForm):
    date = DateField("Date", render_kw={"class": "form-control"}, format='%Y%m%d')
    weight = FloatField("Weight", render_kw={"class": "form-control", "pattern": "[0-9]+([\.,][0-9]+)?", "step": "0.01"})
    submit = SubmitField("Submit", render_kw={"class": "btn bnt-lg btn-dark"})


class ShipmentSpendingController:
    def __init__(self):
        shipment_prices = ShipmentPrice.query.filter(ShipmentPrice.end == None).all()
        current_app.logger.info(f"below are retrieved shipment prices : {shipment_prices}")
        if len(shipment_prices) > 0:
            self.shipment_per_kg_price = shipment_prices[0].price
        else:
            self.shipment_per_kg_price = 2000

    def show_all_spendings(self):
        records = ShipmentSpending.query.order_by(ShipmentSpending.date.desc()).all()
        df = pd.read_sql(ShipmentSpending.query.statement, ShipmentSpending.query.session.bind)
        total_amount = df['amount'].sum()
        return render_template("shipment_spending/shipment_spending_main.html", records=records, total_amount=total_amount, title="Shipment spendings")

    def add_shipment_spending(self):
        form = ShipmentSpendingForm()
        if form.validate_on_submit():
            date = form.date.data
            weight = form.weight.data
            amount = weight * self.shipment_per_kg_price
            new_record = ShipmentSpending(date=date, weight=weight, amount=amount)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Successfully added {date}, {weight}, {amount}", "success")
            return self.show_all_spendings()
        form.date.data = datetime.date.today()
        return render_template("shipment_spending/shipment_spending_add.html", form=form, title="Add shipment spending")

    def edit_shipment_spending(self, id):
        record = ShipmentSpending.query.get(id)
        form = ShipmentSpendingForm()
        if form.validate_on_submit():
            date = form.date.data
            weight = form.weight.data
            amount = weight * self.shipment_per_kg_price
            record.date = date
            record.weight = weight
            record.amount = amount
            db.session.commit()
            flash(f"Updated to {date},{weight},{amount}", "success")
            return self.show_all_spendings()
        form.date.data = record.date
        form.weight.data = record.weight
        return render_template("shipment_spending/shipment_spending_edit.html", form=form, title="Edit shipment spending")

    def remove_shipment_spending(self, id):
        record = ShipmentSpending.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed id {id}", "success")
        return self.show_all_spendings()
