import os
from application import db,moment
from application import images
from flask import render_template, redirect, flash, current_app, request,url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import daily_spending_bp
from .forms import SpendingForm
from .models import Spending,SpendingCategory,PaymentMethod
import datetime
from .receipt_process import extract_receipt_image_as_gray,save_receipt_image_and_update_spending_db_record
import shutil
import pathlib
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from dateutil import tz

@daily_spending_bp.app_context_processor
def inject_tz_conversion_functions():
    def utc_to_localtz(_datetime):
        utc = tz.gettz('UTC')
        localtz = tz.tzlocal()

        utctime = _datetime.replace(tzinfo=utc)
        localtime = utctime.astimezone(localtz)
        return localtime
    
    def localtz_to_utc(_datetime):
        utc = tz.gettz('UTC')
        localtz = tz.tzlocal()

        localtime = _datetime.replace(tzinfo=localtz)        
        utctime = localtime.astimezone(utc)
        
        return utctime

    return dict(utc_to_localtz=utc_to_localtz,localtz_to_utc=localtz_to_utc)

def utc_to_localtz(_datetime):
    utc = tz.gettz('UTC')
    localtz = tz.tzlocal()

    utctime = _datetime.replace(tzinfo=utc)
    localtime = utctime.astimezone(localtz)
    return localtime


def localtz_to_utc(_datetime):
    return datetime.datetime.utcfromtimestamp(_datetime.timestamp())


@daily_spending_bp.app_context_processor
def inject_utc_to_jst():
    def utc_to_jst(_datetime):
        utc = tz.gettz('UTC')
        localtz = tz.gettz('JST')

        utctime = _datetime.replace(tzinfo=utc)
        localtime = utctime.astimezone(localtz)
        return localtime
    return dict(utc_to_jst=utc_to_jst)


def save_spending_record_from_form(form:FlaskForm,db:SQLAlchemy):
    spending = Spending(spent_at=localtz_to_utc(form.spent_at.data),
                        name=form.name.data,
                        amount=form.amount.data,
                        spending_category_id=form.spending_category.data,
                        payment_method_id=form.payment_method.data)        
    
    db.session.add(spending)
    db.session.commit()
    return spending

def update_spending_record_from_form(form:FlaskForm,spending,db:SQLAlchemy):
    spending.spent_at=localtz_to_utc(form.spent_at.data),
    spending.name=form.name.data,
    spending.amount=form.amount.data,
    spending.spending_category_id=form.spending_category.data,
    spending.payment_method_id=form.payment_method.data
    spending.modified_at=localtz_to_utc(datetime.datetime.now())
    db.session.add(spending)
    db.session.commit()
    return spending

def populate_spending_form_category_and_payment_methods(form:FlaskForm):
    form.spending_category.choices=[(spending_category.id,spending_category.name) for spending_category in SpendingCategory.query.all()]
    form.payment_method.choices=[(payment_method.id,payment_method.name) for payment_method in PaymentMethod.query.all()]
    return form

@daily_spending_bp.route("/daily_spending/home")
@login_required
def daily_spending_home():
    return render_template("spending_home.html")

@daily_spending_bp.route("/daily_spending/new",methods=["GET","POST"])
@login_required
def daily_spending_new():
    form = SpendingForm()
    form=populate_spending_form_category_and_payment_methods(form)
    if form.validate_on_submit():
        spending = save_spending_record_from_form(form,db)
        if form.receipt_image.data:
            save_receipt_image_and_update_spending_db_record(form,spending,images,db)
        flash(f"saved {spending} successfully","success")
        return redirect(url_for("daily_spending_bp.daily_spending"))    
    return render_template("generic_form.html",form=form)


@daily_spending_bp.route("/daily_spending")
@login_required
def daily_spending():
    now=datetime.datetime.now()
    year,month=now.year,now.month
    month_beginning=datetime.datetime(now.year,now.month,1)
    spendings = Spending.query.filter(Spending.spent_at>=month_beginning)
    total_amount=sum([spending.amount for spending in spendings])
    summary_year_monthes=[(year,month)]
    s_year,s_month=year,month
    for i in range(1,4):
        s_year=year
        s_month=s_month-1
        if s_month<1:
            s_year=s_year-1
            s_month=12
        summary_year_monthes.append((s_year,s_month))

    return render_template("spendings.html",spendings=spendings,total_amount=total_amount,spending_year=year,spending_month=month,summary_year_monthes=summary_year_monthes)

@daily_spending_bp.route("/daily_spending/all")
@login_required
def daily_spending_all():
    spendings = Spending.query.all()
    total_amount=sum([spending.amount for spending in spendings])
    return render_template("spendings.html",spendings=spendings,total_amount=total_amount)


@daily_spending_bp.route("/daily_spending/<id>")
@login_required
def one_daily_spending(id:int):
    spending=Spending.query.get(id)    
    return render_template("spending.html",spending=spending)

@daily_spending_bp.route("/daily_spending/edit/<id>",methods=["GET","POST"])
def daily_spending_edit(id:int):
    spending=Spending.query.get(id)
    form = SpendingForm()
    form = populate_spending_form_category_and_payment_methods(form)
    if form.validate_on_submit():
        spending = update_spending_record_from_form(form,spending,db)
        if form.receipt_image.data:
            save_receipt_image_and_update_spending_db_record(form,spending,images,db)
        flash(f"Updated {spending}","success")
        return redirect(url_for("daily_spending_bp.daily_spending"))
    form.spent_at.data=utc_to_localtz(spending.spent_at)
    form.name.data=spending.name
    form.amount.data=spending.amount
    form.spending_category.data=spending.spending_category_id
    form.payment_method.data=spending.payment_method_id
    return render_template("generic_form.html",form=form)

@daily_spending_bp.route("/daily_spending/delete/<id>")
def daily_spending_delete(id:int):
    spending=Spending.query.get(id)
    db.session.delete(spending)
    db.session.commit()
    flash(f"removed the record","success")
    return redirect(url_for("daily_spending_bp.daily_spending"))


import calendar
import pandas as pd
@daily_spending_bp.route("/daily_spending/<year>/<month>")
def daily_spending_summary_year_month(year:int,month:int):
    year,month=int(year),int(month)   
    month_begin_weekday,month_no_days=calendar.monthrange(year,month)
    month_beginning = datetime.datetime(year, month,1)
    month_ending = datetime.date(year,month,month_no_days)
    spendings = Spending.query.filter(Spending.spent_at>=month_beginning).filter(Spending.spent_at<=month_ending)
    total_amount=sum([spending.amount for spending in spendings])
    category_amount=[{"spending_category":spending.spending_category.name,"amount":spending.amount} for spending in spendings]
    ca_df=pd.DataFrame(category_amount)
    ca_summary_series = ca_df.groupby("spending_category")["amount"].sum()
    ca_summary_list=[(category,amount) for category,amount in zip(ca_summary_series.index,ca_summary_series.values)]
    return render_template("spending_summary_year_month.html",ca_summary_list=ca_summary_list,total_amount=total_amount)
