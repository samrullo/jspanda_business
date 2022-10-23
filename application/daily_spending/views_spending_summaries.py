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
import calendar
import pandas as pd
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from dateutil import tz

def get_category_name_to_id_mapping():
    categories=SpendingCategory.query.all()
    return {category.name:category.id for category in categories}

def get_group_by_item_amount_as_tuples(items_df,grp_by_col,amount_col):
    grp_series=items_df.groupby(grp_by_col)[amount_col].sum()
    grp_by_list=[(grp_by,amount)for grp_by,amount in zip(grp_series.index,grp_series.values)]
    return grp_by_list

@daily_spending_bp.route("/daily_spending/<year>/<month>")
@login_required
def daily_spending_summary_year_month(year:int,month:int):
    year,month=int(year),int(month)   
    month_begin_weekday,month_no_days=calendar.monthrange(year,month)
    month_beginning = datetime.datetime(year, month,1)
    month_ending = datetime.date(year,month,month_no_days)
    spendings = Spending.query.filter(Spending.spent_at>=month_beginning).filter(Spending.spent_at<=month_ending)
    total_amount=sum([spending.amount for spending in spendings])
    category_amount=[{"spending_category":spending.spending_category.name,"amount":spending.amount} for spending in spendings]
    ca_df=pd.DataFrame(category_amount)    
    ca_summary_list=get_group_by_item_amount_as_tuples(ca_df,"spending_category","amount")
    category_name_to_id=get_category_name_to_id_mapping()
    return render_template("spending_summary_year_month.html",ca_summary_list=ca_summary_list,total_amount=total_amount,spending_year=year,spending_month=month,category_name_to_id=category_name_to_id)

@daily_spending_bp.route("/daily_spending/details/<year>/<month>")
@login_required
def daily_spending_details_year_month(year:int,month:int):
    year,month=int(year),int(month)   
    month_begin_weekday,month_no_days=calendar.monthrange(year,month)
    month_beginning = datetime.datetime(year, month,1)
    month_ending = datetime.date(year,month,month_no_days)
    spendings = Spending.query.filter(Spending.spent_at>=month_beginning).filter(Spending.spent_at<=month_ending)
    total_amount=sum([spending.amount for spending in spendings])
    return render_template("spending_details.html",spendings=spendings,total_amount=total_amount,spending_year=year,spending_month=month)

@daily_spending_bp.route("/daily_spending/details/<category_id>/<year>/<month>")
@login_required
def daily_spending_details_category_year_month(category_id:int,year:int,month:int):
    category_id,year,month = int(category_id),int(year),int(month)
    category = SpendingCategory.query.get(category_id)  
    month_begin_weekday,month_no_days=calendar.monthrange(year,month)
    month_beginning = datetime.datetime(year, month,1)
    month_ending = datetime.date(year,month,month_no_days)
    spendings = Spending.query.filter(Spending.spent_at>=month_beginning).filter(Spending.spent_at<=month_ending).filter(Spending.spending_category_id==category_id)
    total_amount=sum([spending.amount for spending in spendings])
    return render_template("spending_details_category_year_month.html",spendings=spendings,total_amount=total_amount,category=category,spending_year=year,spending_month=month)



@daily_spending_bp.route("/daily_spending/summary/category/<category_id>/<year>/<month>")
@login_required
def daily_spending_summary_category_by_names_year_month(category_id:int, year:int, month:int):
    category_id,year,month = int(category_id),int(year),int(month)
    category = SpendingCategory.query.get(category_id)  
    month_begin_weekday,month_no_days=calendar.monthrange(year,month)
    month_beginning = datetime.datetime(year, month,1)
    month_ending = datetime.date(year,month,month_no_days)
    spendings = Spending.query.filter(Spending.spent_at>=month_beginning).filter(Spending.spent_at<=month_ending).filter(Spending.spending_category_id==category_id)
    name_amounts=[{"name":spending.name.upper(),"amount":spending.amount} for spending in spendings]
    df = pd.DataFrame(name_amounts)
    summary_list=get_group_by_item_amount_as_tuples(df,"name","amount")
    total_amount=sum([spending.amount for spending in spendings])    
    return render_template("spending_summary_category_by_name_year_month.html",summary_list=summary_list,total_amount=total_amount,spending_year=year,spending_month=month,category=category.name)
