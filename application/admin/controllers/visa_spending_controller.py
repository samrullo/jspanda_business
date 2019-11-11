import datetime
from application.admin.models.visa_spendings import VisaSpending, db
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, IntegerField, DateField
from application.utils.utils import to_yyyymmdd

logger = logging.getLogger(__name__)


class VisaSpendingForm(FlaskForm):
    visa = StringField("Visa", render_kw={"class": "form-control"})
    date = DateField("Date", render_kw={"class": "form-control"}, format='%Y%m%d')
    amount = IntegerField("Amount", render_kw={"class": "form-control", "pattern": "[0-9]*"})
    submit = SubmitField("Submit", render_kw={"class": "btn bnt-lg btn-dark"})


class VisaSpendingController:
    def __init__(self):
        self.name = ""

    def show_visa_spendings_by_date(self, adate):
        records = VisaSpending.query.filter(VisaSpending.date == datetime.datetime.strptime(adate, '%Y-%m-%d')).all()
        df = pd.read_sql(VisaSpending.query.filter(VisaSpending.date == datetime.datetime.strptime(adate, '%Y-%m-%d')).statement, VisaSpending.query.filter(VisaSpending.date == datetime.datetime.strptime(adate, '%Y-%m-%d')).session.bind)
        total_amount = df['amount'].sum()
        return render_template("visa_spending/visa_spending_by_date.html", records=records, total_amount=total_amount, title=f"Visa spendings as of {adate} ")

    def show_visa_spendings(self):
        df = pd.read_sql(VisaSpending.query.statement, VisaSpending.query.session.bind)
        visa_df = df.groupby('date').sum()[['amount']]
        visa_df.sort_index(ascending=False, inplace=True)
        total_amount = df['amount'].sum()
        return render_template("visa_spending/visa_spending_main.html", visa_df=visa_df, total_amount=total_amount, title="Visa spendings")

    def add_visa_spending(self):
        form = VisaSpendingForm()
        if form.validate_on_submit():
            date = form.date.data
            visa = form.visa.data
            amount = form.amount.data
            new_record = VisaSpending(date=date, visa=visa, amount=amount)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Successfully added {date}, {visa}, {amount}", "success")
            return self.show_visa_spendings()
        form.date.data = datetime.date.today()
        return render_template("visa_spending/visa_spending_add.html", form=form, title="Add visa spending")

    def edit_visa_spending(self, id):
        record = VisaSpending.query.get(id)
        form = VisaSpendingForm()
        if form.validate_on_submit():
            date = form.date.data
            visa = form.visa.data
            amount = form.amount.data
            record.date = date
            record.visa = visa
            record.amount = amount
            db.session.commit()
            flash(f"Updated to {date},{visa},{amount}", "success")
            return self.show_visa_spendings()
        form.date.data = record.date
        form.visa.data = record.visa
        form.amount.data = record.amount
        return render_template("visa_spending/visa_spending_edit.html", form=form, title="Edit visa spending")

    def remove_visa_spending(self, id):
        record = VisaSpending.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed id {id}", "success")
        return self.show_visa_spendings()
