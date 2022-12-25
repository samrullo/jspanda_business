from . import jspanda_orders_bp
from application.jspanda_orders.models.jspanda_order import JspandaOrderDebtAllocation,JspandaOrderDebt, db
from application.admin.models.received_money_model import ReceivedMoney
from flask import render_template
from flask_login import login_required
from flask import redirect, url_for
from flask import flash
from datetime import datetime
from application.jspanda_orders.forms.jspanda_order_forms import JspandaOrderDebtAllocationForm
from application.utils.utils import DotDict

def evaluate_if_jspanda_debt_is_paid(jspanda_debt):
    debt_allocations = JspandaOrderDebtAllocation.query.filter_by(jspanda_order_debt_id=jspanda_debt.id).all()
    if len(debt_allocations)>0:
        allocated_amount = sum([record.allocated_amount for record in debt_allocations])
    else:
        allocated_amount = 0
    return jspanda_debt.amount_usd == allocated_amount

def evaluate_if_received_money_is_allocated(received_money):
    debt_allocations = JspandaOrderDebtAllocation.query.filter_by(received_money_id=received_money.id).all()
    if len(debt_allocations)>0:
        allocated_amount = sum([record.allocated_amount for record in debt_allocations])
    else:
        allocated_amount = 0
    return received_money.amount_usd == allocated_amount

def evaluate_if_over_allocating_received_money(received_money,allocated_amount):
    return allocated_amount > received_money.amount_usd

def evaluate_if_over_paying_jspanda_debt(jspanda_debt,allocated_amount):
    debt_allocations = JspandaOrderDebtAllocation.query.filter_by(jspanda_order_debt_id=jspanda_debt.id).all()
    if len(debt_allocations)>0:
        current_allocated_amount = sum([record.allocated_amount for record in debt_allocations])
    else:
        current_allocated_amount = 0
    return current_allocated_amount+allocated_amount>jspanda_debt.amount_usd

@jspanda_orders_bp.route("/jspanda/debt/allocations")
@login_required
def debt_allocations():
    records=JspandaOrderDebtAllocation.query.all()    
    col_names=[
               DotDict({"description":"Jspanda Debt","db_name":"jspanda_order_debt","type":"text"}),
               DotDict({"description":"Received Money","db_name":"received_money","type":"text"}),
               DotDict({"description":"Allocated Amount","db_name":"allocated_amount","type":"numeric"}),
               DotDict({"description":"Created At","db_name":"created_at","type":"datetime"}),
               DotDict({"description":"Modified At","db_name":"modified_at","type":"datetime"})
               ]
    return render_template("generic_table.html",title="Debt Allocations",order_by_col_no=4,col_names=col_names,records=records,summary_records=None,add_func_name='jspanda_orders_bp.debt_allocation_new',
    edit_func_name='jspanda_orders_bp.debt_allocation_edit',
    remove_func_name='jspanda_orders_bp.debt_allocation_remove')


@jspanda_orders_bp.route("/jspanda/debt/allocation/new", methods=['GET','POST'])
@login_required
def debt_allocation_new():
    form = JspandaOrderDebtAllocationForm()
    if form.validate_on_submit():
        allocated_amount=form.allocated_amount.data
        jspanda_debt = JspandaOrderDebt.query.get(form.jspanda_order_debt.data)
        received_money=ReceivedMoney.query.get(form.received_money.data)
        if evaluate_if_over_allocating_received_money(received_money,allocated_amount):
            flash(f"Over allocating {received_money} with {allocated_amount}","danger")
        elif evaluate_if_over_paying_jspanda_debt(jspanda_debt,allocated_amount):
            flash(f"Over paying {jspanda_debt} with {allocated_amount}")
        else:
            record=JspandaOrderDebtAllocation(allocated_amount=form.allocated_amount.data,jspanda_order_debt_id=form.jspanda_order_debt.data,received_money_id=form.received_money.data)
            db.session.add(record)
            db.session.commit()
            flash(f"Added {record} successfully","success")

            jspanda_order_debt=record.jspanda_order_debt
            received_money=record.received_money
            if evaluate_if_jspanda_debt_is_paid(jspanda_order_debt):
                jspanda_order_debt.is_paid=True
            else:
                jspanda_order_debt.is_paid=False
            db.session.add(jspanda_order_debt)
            db.session.commit()

            if evaluate_if_received_money_is_allocated(received_money):
                received_money.is_allocated=True
            else:
                received_money.is_allocated=False
            db.session.add(received_money)
            db.session.commit()
            return redirect(url_for('jspanda_orders_bp.debt_allocations'))
    pending_debts=JspandaOrderDebt.query.filter_by(is_paid=False).all()
    received_moneys = ReceivedMoney.query.filter_by(is_for_debt=True).filter_by(is_allocated=False).all()
    form.jspanda_order_debt.choices=[(pending_debt.id,pending_debt) for pending_debt in pending_debts]
    form.received_money.choices=[(received_money.id,received_money) for received_money in received_moneys]
    return render_template("generic_form.html",form=form,title="New debt allocation")


@jspanda_orders_bp.route("/jspanda/debt/allocation/edit/<id>", methods=['GET','POST'])
@login_required
def debt_allocation_edit(id:int):
    record = JspandaOrderDebtAllocation.query.get(id)
    # since we will be editing we change is_paid and is_allocated values of this debt allocation record's 
    # corresponding debt and received money to false
    record.jspanda_order_debt.is_paid=False
    record.received_money.is_allocated=False
    db.session.add(record.jspanda_order_debt)
    db.session.commit()
    db.session.add(record.received_money)
    db.session.commit()
    form = JspandaOrderDebtAllocationForm()
    if form.validate_on_submit():
        allocated_amount=form.allocated_amount.data
        jspanda_debt = JspandaOrderDebt.query.get(form.jspanda_order_debt.data)
        received_money=ReceivedMoney.query.get(form.received_money.data)
        if evaluate_if_over_allocating_received_money(received_money,allocated_amount):
            flash(f"Over allocating {received_money} with {allocated_amount}","danger")
        elif evaluate_if_over_paying_jspanda_debt(jspanda_debt,allocated_amount):
            flash(f"Over paying {jspanda_debt} with {allocated_amount}")
        else:     
            record.allocated_amount=form.allocated_amount.data
            record.received_money_id=form.received_money.data
            record.jspanda_order_debt_id=form.jspanda_order_debt.data
            record.modified_at=datetime.utcnow()
            db.session.add(record)
            db.session.commit()
            flash(f"Edited {record} successfully","success")

            jspanda_order_debt=record.jspanda_order_debt
            received_money=record.received_money
            if evaluate_if_jspanda_debt_is_paid(jspanda_order_debt):
                jspanda_order_debt.is_paid=True
            else:
                jspanda_order_debt.is_paid=False
            db.session.add(jspanda_order_debt)
            db.session.commit()


            if evaluate_if_received_money_is_allocated(received_money):
                received_money.is_allocated=True
            else:
                received_money.is_allocated=False
            db.session.add(received_money)
            db.session.commit()
            return redirect(url_for('jspanda_orders_bp.debt_allocations'))
    pending_debts=JspandaOrderDebt.query.filter_by(is_paid=False).all()
    pending_debts = sorted(pending_debts,key=lambda record : record.date)
    received_moneys = ReceivedMoney.query.filter_by(is_for_debt=True).filter_by(is_allocated=False).all()
    received_moneys = sorted(received_moneys,key=lambda record : record.registered_date)
    form.jspanda_order_debt.choices=[(pending_debt.id,pending_debt) for pending_debt in pending_debts]
    form.received_money.choices=[(received_money.id,received_money) for received_money in received_moneys]

    form.allocated_amount.data=record.allocated_amount
    form.received_money.data=record.received_money_id
    form.jspanda_order_debt.data=record.jspanda_order_debt_id

    return render_template("generic_form.html",form=form,title="Edit debt allocation")


@jspanda_orders_bp.route("/jspanda/debt/allocation/remove/<id>", methods=['GET','POST'])
@login_required
def debt_allocation_remove(id:int):
    record = JspandaOrderDebtAllocation.query.get(id)

    # since we are removing a debt allocation we are setting is_paid attribute to False
    jspanda_order_debt=record.jspanda_order_debt
    received_money=record.received_money    
    jspanda_order_debt.is_paid=False
    db.session.add(jspanda_order_debt)
    db.session.commit()
    # and is_allocated to False
    received_money.is_allocated=False
    db.session.add(received_money)
    db.session.commit()
    

    db.session.delete(record)
    db.session.commit()
    flash(f"Removed {record} successfully")
    return redirect(url_for('jspanda_orders_bp.debt_allocations'))
