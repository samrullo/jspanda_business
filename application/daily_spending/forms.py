from flask_wtf import FlaskForm
from wtforms import StringField,DateTimeField,IntegerField,SelectField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed
import datetime
from application import images

class SpendingForm(FlaskForm):
    spent_at=DateTimeField("Spent At",default=datetime.datetime.now,render_kw={"class":"form-control"})
    name=StringField("Spending Name",render_kw={"class":"form-control"})
    amount = IntegerField("Spent Amount",render_kw={"class":"form-control"})
    spending_category=SelectField("Spending Category",coerce=int,validate_choice=False,render_kw={"class":"form-control"})
    payment_method=SelectField("Payment Method", coerce=int,validate_choice=False,render_kw={"class":"form-control"})
    receipt_image=FileField("Reciept Image", validators=[FileAllowed(images,'Images only are allowed (optional) (.jpg, .jpe, .jpeg, .png, .gif, .svg, and .bmp)!')],render_kw={"class":"form-control-file"})
    submit = SubmitField("Submit",render_kw={"class":"btn btn-dark"})

class SpendingCategoryForm(FlaskForm):
    name = StringField("Category Name",render_kw={"class":"form-control"})
    submit = SubmitField("Submit",render_kw={"class":"btn btn-dark"})

class PaymentMethodForm(FlaskForm):
    name = StringField("Payment Method",render_kw={"class":"form-control"})
    submit = SubmitField("Submit",render_kw={"class":"btn btn-dark"})