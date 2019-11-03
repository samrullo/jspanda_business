import datetime
from application.admin.models.received_money_model import ReceivedMoney, db
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateField
from application.utils.utils import to_yyyymmdd


class ReceivedMoneyForm(FlaskForm):
    id = HiddenField("id")
    date = DateField("date", render_kw={"class": "form-control"}, format='%Y%m%d')
    amount_usd = StringField("amount_usd", render_kw={"class": "form-control", "pattern": "[0-9]*"})
    exchange_rate = StringField("exchange_rate", render_kw={"class": "form-control"})
    submit = SubmitField("Save received money", render_kw={"class": "btn btn-lg btn-dark"})


class ReceivedMoneyController:

    def show_all_received_money(self):
        received_money_records = ReceivedMoney.query.order_by(ReceivedMoney.registered_date.desc()).all()
        # logging.info(f"Received money records : {received_money_records}")
        df = pd.read_sql(ReceivedMoney.query.statement, ReceivedMoney.query.session.bind)
        total_amount_usd = df['amount_usd'].sum()
        total_amount_jpy = df['amount_jpy'].sum()
        average_exchange_rate = df['exchange_rate'].mean()
        return render_template("received_money/received_money_main.html", received_money_records=received_money_records, total_amount_usd=total_amount_usd, total_amount_jpy=total_amount_jpy, average_exchange_rate=average_exchange_rate, title="Received money")

    def add_received_money(self):
        form = ReceivedMoneyForm()
        logging.info(f"form hidden tag : {form.hidden_tag()}")
        if form.validate_on_submit():
            date = form.date.data
            amount_usd = int(form.amount_usd.data)
            exchange_rate = float(form.exchange_rate.data)
            amount_jpy = amount_usd * exchange_rate
            new_received_money_record = ReceivedMoney(registered_date=to_yyyymmdd(date), amount_usd=amount_usd, exchange_rate=exchange_rate, amount_jpy=amount_jpy)
            db.session.add(new_received_money_record)
            db.session.commit()
            flash(f"Saved {date} {amount_usd} {exchange_rate} successfully", "success")
            return self.show_all_received_money()
        return render_template("received_money/received_money_add.html", form=form, title="Add received money")

    def edit_received_money(self, id):
        form = ReceivedMoneyForm()
        received_money = ReceivedMoney.query.get(id)
        if form.validate_on_submit():
            date = form.date.data
            amount_usd = int(form.amount_usd.data)
            exchange_rate = float(form.exchange_rate.data)

            # update the record
            received_money.registered_date = date
            received_money.amount_usd = amount_usd
            received_money.exchange_rate = exchange_rate
            received_money.amount_jpy = amount_usd * exchange_rate
            db.session.commit()
            flash(f"Updated {form.id.data} to {date},{amount_usd},{exchange_rate} successfully", "success")
            return self.show_all_received_money()
        form.id.data = received_money.id
        form.date.data = received_money.registered_date
        form.amount_usd.data = received_money.amount_usd
        form.exchange_rate.data = received_money.exchange_rate
        form.submit.data = "Update received money"
        return render_template("received_money/received_money_edit.html", form=form, title="Edit received money")

    def remove_received_money(self, id):
        received_money = ReceivedMoney.query.get(id)
        db.session.delete(received_money)
        db.session.commit()
        flash(f"Successfully removed {id} record", "success")
        return self.show_all_received_money()
