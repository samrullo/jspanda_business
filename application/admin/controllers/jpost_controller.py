import datetime
from application.admin.models.jpost_spending import JpostSpending, db
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, IntegerField, DateField, FloatField
from application.utils.utils import to_yyyymmdd


class JpostSpendingForm(FlaskForm):
    date = DateField("Date", render_kw={"class": "form-control"}, format='%Y%m%d')
    order_date = DateField("Order Date", render_kw={"class": "form-control"}, format='%Y%m%d')
    amount = IntegerField("Yubin spending", render_kw={"class": "form-control", "pattern": "[0-9]+([\.,][0-9]+)?", "step": "0.01"})
    submit = SubmitField("Submit", render_kw={"class": "btn bnt-lg btn-dark"})


class JpostSpendingController:
    def __init__(self):
        self.shipment_per_kg_price = 1500

    def show_all_spendings(self):
        records = JpostSpending.query.order_by(JpostSpending.date.desc()).all()
        df = pd.read_sql(JpostSpending.query.statement, JpostSpending.query.session.bind)
        total_amount = df['amount'].sum()
        return render_template("jpost_spending/jpost_spending_main.html", records=records, total_amount=total_amount, title="Yubin spendings")

    def add_jpost_spending(self):
        form = JpostSpendingForm()
        if form.validate_on_submit():
            new_record = JpostSpending(date=form.date.data, order_date=form.order_date.data, amount=form.amount.data)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Successfully added {new_record.date}, {new_record.order_date}, {new_record.amount}", "success")
            return self.show_all_spendings()
        form.date.data = datetime.date.today()
        form.order_date.data = datetime.date.today()
        return render_template("jpost_spending/jpost_spending_add.html", form=form, title="Add yubin spending")

    def edit_jpost_spending(self, id):
        record = JpostSpending.query.get(id)
        form = JpostSpendingForm()
        if form.validate_on_submit():
            record.date = form.date.data
            record.order_date = form.order_date.data
            record.amount = form.amount.data
            db.session.commit()
            flash(f"Updated to {record.date},{record.order_date},{record.amount}", "success")
            return self.show_all_spendings()
        form.date.data = record.date
        form.order_date.data = record.order_date
        form.amount.data = record.amount
        return render_template("jpost_spending/jpost_spending_edit.html", form=form, title="Edit jpost spending")

    def remove_jpost_spending(self, id):
        record = JpostSpending.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed id {id}", "success")
        return self.show_all_spendings()
