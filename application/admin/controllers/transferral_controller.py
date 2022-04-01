import datetime
from application.admin.models.transferrals import Transferral, db
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, IntegerField, DateField
from application.utils.utils import to_yyyymmdd

logger = logging.getLogger(__name__)


class TransferralForm(FlaskForm):
    date = DateField("Date", render_kw={"class": "form-control"})
    amount = IntegerField("Amount", render_kw={"class": "form-control", "pattern": "[0-9]*"})
    submit = SubmitField("Submit", render_kw={"class": "btn bnt-lg btn-dark"})


class TransferralController:
    def __init__(self):
        self.name = ""

    def show_transferrals(self):
        records = Transferral.query.order_by(Transferral.date.desc()).all()
        df = pd.read_sql(Transferral.query.statement, Transferral.query.session.bind)
        total_amount = df['amount'].sum()
        return render_template("transferral/transferral_main.html", records=records, total_amount=total_amount, title="Transferrals")

    def show_monthly_transferrals(self):
        records = Transferral.query.all()
        transferrals_df = pd.DataFrame(columns=['date', 'amount'], data=[(record.date, record.amount) for record in records])
        transferrals_df['year_month'] = transferrals_df['date'].map(lambda adate: datetime.date(adate.year, adate.month, 1))
        grp_transferrals_df = transferrals_df.groupby('year_month')[['amount']].sum()
        grp_transferrals_df = grp_transferrals_df.sort_index(ascending=False)
        return render_template("transferral/transferral_show_monthly.html", grp_transferrals_df=grp_transferrals_df, title="Monthly transferrals", total_amount=transferrals_df['amount'].sum())

    def add_transferral(self):
        form = TransferralForm()
        if form.validate_on_submit():
            date = form.date.data
            amount = form.amount.data
            new_record = Transferral(date=date, amount=amount)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Successfully added {date},{amount}", "success")
            return self.show_transferrals()
        form.date.data = datetime.date.today()
        return render_template("transferral/transferral_add.html", form=form, title="Add transferral")

    def edit_transferral(self, id):
        record = Transferral.query.get(id)
        form = TransferralForm()
        if form.validate_on_submit():
            record.date = form.date.data
            record.amount = form.amount.data
            db.session.commit()
            flash(f"Updated to {record.date},{record.amount}", "success")
            return self.show_transferrals()
        form.date.data = record.date
        form.amount.data = record.amount
        return render_template("transferral/transferral_edit.html", form=form, title="Edit transferral")

    def remove_transferral(self, id):
        record = Transferral.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed id {id}", "success")
        return self.show_transferrals()
