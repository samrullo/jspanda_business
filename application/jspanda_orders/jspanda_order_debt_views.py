from . import jspanda_orders_bp
from application.jspanda_orders.models.jspanda_order import JspandaOrderDebt, JspandaOrderDebtAllocation, db
from flask import render_template
from flask_login import login_required
from flask import redirect, url_for
from flask import flash
import datetime
from application.jspanda_orders.forms.jspanda_order_forms import JspandaOrderDebtForm

from application.utils.utils import DotDict

def calc_paid_debt(jspanda_debt):
    debt_allocations = JspandaOrderDebtAllocation.query.filter_by(jspanda_order_debt_id=jspanda_debt.id).all()
    if len(debt_allocations)>0:
        allocated_amount = sum([record.allocated_amount for record in debt_allocations])
    else:
        allocated_amount = 0
    return allocated_amount

@jspanda_orders_bp.route("/jspanda/order/debts")
@login_required
def jspanda_order_debts():
    records=JspandaOrderDebt.query.all()
    records=[DotDict(record.__dict__) for record in records]
    for record in records:
        record.paid_debt = calc_paid_debt(record)
        record.unpaid_debt = record.amount_usd - record.paid_debt    
    col_names=[DotDict({"description":"Date","db_name":"date","type":"date"}),
              DotDict({"description":"Amount in USD","db_name":"amount_usd","type":"numeric"}),
              DotDict({"description":"Paid Debt","db_name":"paid_debt","type":"numeric"}),
              DotDict({"description":"Unpaid Debt","db_name":"unpaid_debt","type":"numeric"}),
              DotDict({"description":"Is Paid","db_name":"is_paid","type":"boolean"}),
              DotDict({"description":"Created At","db_name":"created_at","type":"datetime"}),
              DotDict({"description":"Modified At","db_name":"modified_at","type":"datetime"})]
    order_by_col_no=0
    title = "Jspanda Order Debts"
    total_unpaid_debt = sum([record.unpaid_debt for record in records])
    summary_records=[DotDict({"description":"Total unpaid debt","type":"numeric","value":total_unpaid_debt})]
    success_col_name="is_paid"
    return render_template("generic_table.html",
                            title=title,
                            order_by_col_no=order_by_col_no,
                            col_names=col_names,
                            records=records,
                            summary_records=summary_records,
                            success_col_name=success_col_name,
                            add_func_name='jspanda_orders_bp.jspanda_order_debt_new',
                            edit_func_name='jspanda_orders_bp.jspanda_order_debt_edit',
                            remove_func_name='jspanda_orders_bp.jspanda_order_debt_remove')

@jspanda_orders_bp.route("/jspanda/order/debt/new",methods=['GET','POST'])
@login_required
def jspanda_order_debt_new():
    form = JspandaOrderDebtForm()
    if form.validate_on_submit():
        jspanda_order_debt=JspandaOrderDebt(date=form.date.data,amount_usd=form.amount_usd.data,is_paid=form.is_paid.data)
        db.session.add(jspanda_order_debt)
        db.session.commit()
        flash(f"Added new jspanda order debt {jspanda_order_debt.date},{jspanda_order_debt.amount_usd} USD successfully","success")
        return redirect(url_for('jspanda_orders_bp.jspanda_order_debts'))
    form.date.data=datetime.date.today()
    return render_template("generic_form.html",title="New Jspanda Order Debt", form=form)

@jspanda_orders_bp.route("/jspanda/order/debt/edit/<id>",methods=['GET','POST'])
@login_required
def jspanda_order_debt_edit(id:int):
    record = JspandaOrderDebt.query.get(id)
    form = JspandaOrderDebtForm()
    if form.validate_on_submit():
        record.date=form.date.data
        record.amount_usd=form.amount_usd.data        
        record.is_paid=form.is_paid.data
        record.modified_at=datetime.datetime.utcnow()
        db.session.add(record)
        db.session.commit()
        flash(f"Edited jspanda order debt {record.date},{record.amount_usd} USD successfully","success")
        return redirect(url_for('jspanda_orders_bp.jspanda_order_debts'))
    form.date.data=record.date
    form.amount_usd.data=record.amount_usd    
    form.is_paid.data=record.is_paid
    return render_template("generic_form.html",title="New Jspanda Order Debt", form=form)

@jspanda_orders_bp.route("/jspanda/order/debt/remove/<id>", methods=['GET','POST'])
@login_required
def jspanda_order_debt_remove(id:int):
    record = JspandaOrderDebt.query.get(id)
    db.session.delete(record)
    db.session.commit()
    flash(f"Removed {record} successfully")
    return redirect(url_for('jspanda_orders_bp.jspanda_order_debts'))
