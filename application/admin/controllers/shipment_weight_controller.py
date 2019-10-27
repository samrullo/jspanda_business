import datetime
from application.admin.models.shipment_weight import ShipmentWeight, db
import logging
import pandas as pd
import numpy as np
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, IntegerField, DateField, FloatField
from application.utils.utils import to_yyyymmdd


class ShipmentWeightForm(FlaskForm):
    date = DateField("Date", render_kw={"class": "form-control"}, format='%Y%m%d')
    to_whom = StringField("To whom", render_kw={"class": "form-control"})
    weight = FloatField("Weight", render_kw={"class": "form-control", "pattern": "[0-9]+([\.,][0-9]+)?", "step": "0.01"})
    # pattern="[0-9]+([\.,][0-9]+)?" step="0.01"
    #
    submit = SubmitField("Submit", render_kw={"class": "btn bnt-lg btn-dark"})


class ShipmentWeightController:
    def __init__(self):
        self.shipment_per_kg_price = 1500

    def show_pending_shipment_weights(self):
        records = ShipmentWeight.query.filter(ShipmentWeight.is_paid == False).order_by(ShipmentWeight.date.desc()).all()
        df = pd.read_sql(ShipmentWeight.query.statement, ShipmentWeight.query.session.bind)
        total_weight = df.loc[np.logical_not(df.is_paid), 'weight'].sum()
        total_amount = df.loc[np.logical_not(df.is_paid), 'amount'].sum()
        return render_template("shipment_weight/shipment_weight_main.html", records=records, total_amount=total_amount, total_weight=total_weight, title="Pending Shipment weights")

    def show_all_shipment_weights(self):
        records = ShipmentWeight.query.order_by(ShipmentWeight.date.desc()).all()
        df = pd.read_sql(ShipmentWeight.query.statement, ShipmentWeight.query.session.bind)
        total_weight = df['weight'].sum()
        total_amount = df['amount'].sum()
        return render_template("shipment_weight/view_all_shipment_weight.html", records=records, total_amount=total_amount, total_weight=total_weight, title="All Shipment weights")

    def add_shipment_weight(self):
        form = ShipmentWeightForm()
        if form.validate_on_submit():
            date = form.date.data
            to_whom = form.to_whom.data
            weight = form.weight.data
            amount = weight * self.shipment_per_kg_price
            new_record = ShipmentWeight(date=date, to_whom=to_whom, weight=weight, amount=amount, is_paid=False)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Successfully added {date}, {weight}, {amount}", "success")
            return self.show_pending_shipment_weights()
        form.date.data = datetime.date.today()
        form.to_whom.data = "Sabina"
        return render_template("shipment_weight/shipment_weight_add.html", form=form, title="Add shipment weight")

    def edit_shipment_weight(self, id):
        record = ShipmentWeight.query.get(id)
        form = ShipmentWeightForm()
        if form.validate_on_submit():
            date = form.date.data
            to_whom = form.to_whom.data
            weight = form.weight.data
            amount = weight * self.shipment_per_kg_price
            record.date = date
            record.to_whom = to_whom
            record.weight = weight
            record.amount = amount
            db.session.commit()
            flash(f"Updated to {date},{to_whom},{weight},{amount}", "success")
            return self.show_pending_shipment_weights()
        return render_template("shipment_weight/shipment_weight_edit.html", form=form, title="Edit shipment spending")

    def remove_shipment_weight(self, id):
        record = ShipmentWeight.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed id {id}", "success")
        return self.show_pending_shipment_weights()

    def mark_as_paid(self, id):
        record = ShipmentWeight.query.get(id)
        record.is_paid = True
        db.session.commit()
        flash(f"Marked {id} as paid", "success")
        return self.show_pending_shipment_weights()
