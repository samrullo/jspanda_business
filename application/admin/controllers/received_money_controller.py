import datetime
from application.admin.models.received_money_model import ReceivedMoney, db
from application.jspanda_orders.models.jspanda_order import JspandaOrderDebtAllocation
import logging
import pandas as pd
from flask import flash,url_for
from flask import render_template
from flask import redirect
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateField, BooleanField
from application.utils.utils import to_yyyymmdd
from application.utils.utils import DotDict

class ReceivedMoneyForm(FlaskForm):    
    date = DateField("date", render_kw={"class": "form-control"})
    amount_usd = StringField("amount_usd", render_kw={"class": "form-control", "pattern": "[0-9]*"})
    exchange_rate = StringField("exchange_rate", render_kw={"class": "form-control"})
    is_received = BooleanField("Is received", render_kw={"class": "form-check"})
    is_for_debt = BooleanField("Is for debt", render_kw={"class": "form-check"})
    is_allocated = BooleanField("Is allocated", render_kw={"class": "form-check"})
    submit = SubmitField("Save received money", render_kw={"class": "btn btn-lg btn-dark"})


def calc_allocated_amount_for_received_money(received_money):
    debt_allocations=JspandaOrderDebtAllocation.query.filter_by(received_money_id=received_money.id).all()
    if len(debt_allocations)>0:
        allocated_amount = sum([record.allocated_amount for record in debt_allocations])
    else:
        allocated_amount = 0
    return allocated_amount

class ReceivedMoneyController:
    def show_received_money_records(self,received_money_records,title="Received money"):
        records = [DotDict(record.__dict__) for record in received_money_records]
        for record in records:
            record.allocated_amount = calc_allocated_amount_for_received_money(record)
            record.unallocated_amount = record.amount_usd - record.allocated_amount
        
        # logging.info(f"Received money records : {received_money_records}")
        df = pd.read_sql(ReceivedMoney.query.statement, ReceivedMoney.query.session.bind)
        total_amount_usd = df['amount_usd'].sum()
        total_amount_jpy = df['amount_jpy'].sum()
        average_exchange_rate = df['exchange_rate'].mean()
        summary_records = [DotDict({'description':"Total amount in USD",'type':'numeric','value':total_amount_usd}),
                           DotDict({'description':"Total amount in JPY",'type':'numeric','value':total_amount_jpy}),
                           DotDict({'description':"Average exchange rate",'type':'numeric','value':average_exchange_rate})]        
        col_names=[DotDict({"description":"Date","db_name":"registered_date","type":"date"}),
                  DotDict({"description":"Amount in USD","db_name":"amount_usd","type":"numeric"}),
                  DotDict({"description":"Allocated Amount","db_name":"allocated_amount","type":"numeric"}),
                  DotDict({"description":"Unallocated Amount","db_name":"unallocated_amount","type":"numeric"}),
                  DotDict({"description":"Exchange Rate","db_name":"exchange_rate","type":"numeric"}),
                  DotDict({"description":"Amount in JPY","db_name":"amount_jpy","type":"numeric"}),
                  DotDict({"description":"Is Received?","db_name":"is_received","type":"boolean"}),
                  DotDict({"description":"Is For Debt?","db_name":"is_for_debt","type":"boolean"}),
                  DotDict({"description":"Is Allocated?","db_name":"is_allocated","type":"boolean"})]
        extra_funcs=[DotDict({"name":'admin_bp.mark_received_money_as_received',"link_name":"Received"})]
        return render_template("generic_table_with_extra_funcs.html", 
                                title=title,
                                order_by_col_no=0,
                                col_names=col_names,
                                records=records,
                                summary_records=summary_records,
                                success_col_name="is_received",
                                add_func_name="admin_bp.add_received_money",
                                remove_func_name="admin_bp.remove_received_money",
                                edit_func_name="admin_bp.edit_received_money",
                                extra_funcs=extra_funcs)

    def show_all_received_money(self):
        received_money_records = ReceivedMoney.query.order_by(ReceivedMoney.registered_date.desc()).all()
        return self.show_received_money_records(received_money_records)
    
    def show_received_money_for_debt(self):
        received_money_records = ReceivedMoney.query.filter_by(is_for_debt=True).order_by(ReceivedMoney.registered_date.desc()).all()
        return self.show_received_money_records(received_money_records,title="Received money for debt")

    def add_received_money(self):
        form = ReceivedMoneyForm()
        logging.info(f"form hidden tag : {form.hidden_tag()}")
        if form.validate_on_submit():
            date = form.date.data
            amount_usd = int(form.amount_usd.data)
            exchange_rate = float(form.exchange_rate.data)
            amount_jpy = amount_usd * exchange_rate
            new_received_money_record = ReceivedMoney(registered_date=to_yyyymmdd(date), amount_usd=amount_usd, exchange_rate=exchange_rate, amount_jpy=amount_jpy,is_received=form.is_received.data,
                                                      is_for_debt=form.is_for_debt.data,is_allocated=form.is_allocated.data)
            db.session.add(new_received_money_record)
            db.session.commit()
            flash(f"Saved {date} {amount_usd} {exchange_rate} successfully", "success")            
            if new_received_money_record.is_for_debt:
                return redirect(url_for('admin_bp.show_received_money_for_debt'))
            else:
                return redirect(url_for('admin_bp.show_received_money'))
        form.date.data = datetime.date.today()
        return render_template("generic_form.html", form=form, title="Add received money")

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
            received_money.is_received=form.is_received.data
            received_money.is_for_debt=form.is_for_debt.data
            received_money.is_allocated=form.is_allocated.data
            db.session.commit()
            flash(f"Updated {received_money} to {date},{amount_usd},{exchange_rate} successfully", "success")
            if received_money.is_for_debt:
                return redirect(url_for('admin_bp.show_received_money_for_debt'))
            else:
                return redirect(url_for('admin_bp.show_received_money'))            
        form.date.data = received_money.registered_date
        form.amount_usd.data = received_money.amount_usd        
        form.exchange_rate.data = received_money.exchange_rate
        form.is_received.data=received_money.is_received
        form.is_for_debt.data = received_money.is_for_debt
        form.is_allocated.data = received_money.is_allocated
        form.submit.data = "Update received money"
        return render_template("generic_form.html", form=form, title="Edit received money")

    def remove_received_money(self, id):
        received_money = ReceivedMoney.query.get(id)
        db.session.delete(received_money)
        db.session.commit()
        flash(f"Successfully removed {id} record", "success")        
        return redirect(url_for('admin_bp.show_received_money'))
    
    def mark_received_money_as_received(self,id):
        received_money = ReceivedMoney.query.get(id)
        received_money.is_received=True
        db.session.add(received_money)
        db.session.commit()
        flash(f"Successfully marked {received_money} as received","success")
        if received_money.is_for_debt:
            return redirect(url_for('admin_bp.show_received_money_for_debt'))
        else:
            return redirect(url_for('admin_bp.show_received_money'))        
