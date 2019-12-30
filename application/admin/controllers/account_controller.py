import datetime
from application.admin.models.account import Account, db
import logging
import pandas as pd
from flask import flash
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, IntegerField, DateField, FloatField, TextAreaField
from application.utils.utils import to_yyyymmdd


class AccountForm(FlaskForm):
    name = StringField("Name", render_kw={"class": "form-control"})
    pasw = StringField("Pasw", render_kw={"class": "form-control"})
    url = StringField("Url", render_kw={"class": "form-control"})
    extra = TextAreaField("Extra", render_kw={"class": "form-control"})
    date = DateField("Date", render_kw={"class": "form-control"}, format="%Y%m%d")
    submit = SubmitField("Submit", render_kw={"class": "btn btn-dark btn-lg"})


class AccountController:
    def __init__(self):
        self.name = "account controller"

    def show_all_accounts(self):
        records = Account.query.order_by(Account.date.desc()).all()
        return render_template("account/account_main.html", title="Accounts", records=records)

    def add(self):
        form = AccountForm()
        form.date.data = datetime.date.today()
        if form.validate_on_submit():
            new_record = Account(name=form.name.data, pasw=form.pasw.data, url=form.url.data, extra=form.extra.data, date=form.date.data)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Successfull added {str(new_record)}", "success")
            return redirect("/admin/show_all_accounts")
        return render_template("account/account_add.html", title="Add a new account", form=form)

    def edit(self, id):
        record = Account.query.get(id)
        form = AccountForm()
        if form.validate_on_submit():
            record.name = form.name.data
            record.pasw = form.pasw.data
            record.url = form.url.data
            record.date = form.date.data
            record.extra = form.extra.data
            db.session.commit()
            flash(f"Successfully updated {id} to {str(record)}", "success")
            return redirect("/admin/show_all_accounts")
        form.name.data = record.name
        form.pasw.data = record.pasw
        form.url.data = record.url
        form.date.data = record.date
        form.extra.data = record.extra
        return render_template("account/account_edit.html", title="Edit account", form=form)

    def remove(self, id):
        record = Account.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed id {id}", "success")
        return redirect("/admin/show_all_accounts")
