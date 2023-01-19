from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, FloatField, TextAreaField,BooleanField,SelectField

class MortgageForm(FlaskForm):
    borrowed_amount = IntegerField("Borrowed amount",description="amount_usd", render_kw={"class": "form-control"}) 
    interest_rate = FloatField("Interest rate in percentage", description="interest_rate", render_kw={"class":"form-control"})
    borrowing_time = IntegerField("Borrowing time in years",description="amount_usd", render_kw={"class": "form-control"})    
    submit=SubmitField("Submit",description="submit", render_kw={"class": "btn btn-lg btn-dark"})
