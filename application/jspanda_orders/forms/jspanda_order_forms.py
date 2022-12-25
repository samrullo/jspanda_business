from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, FloatField, TextAreaField,BooleanField,SelectField

class JspandaOrderDebtForm(FlaskForm):
    date = DateField("Date",description="date",render_kw={"class": "form-control"})
    amount_usd = IntegerField("Amount in USD",description="amount_usd", render_kw={"class": "form-control"})    
    is_paid = BooleanField("Is paid?", description="is_paid", render_kw={"class": "form-check"})
    submit=SubmitField("Submit",description="submit", render_kw={"class": "btn btn-lg btn-dark"})


class JspandaOrderDebtAllocationForm(FlaskForm):
    jspanda_order_debt = SelectField("Debts",coerce=int,validate_choice=False,choices=[],render_kw={"class":"form-control"})
    received_money = SelectField("Received Money",coerce=int,validate_choice=False,choices=[],render_kw={"class":"form-control"})
    allocated_amount = IntegerField("Allocated amount",render_kw={"class":"form-control"})
    submit=SubmitField("Submit",description="submit", render_kw={"class": "btn btn-lg btn-dark"})