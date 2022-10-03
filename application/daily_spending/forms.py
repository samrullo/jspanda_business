from flask_wtf import FlaskForm
from wtforms import StringField,DateTimeField,IntegerField,SelectField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed
import datetime
from application import images

class SpendingForm(FlaskForm):
    spent_at=DateTimeField("Spent At",default=datetime.datetime.now)
    name=StringField("Spending Name")
    amount = IntegerField("Spent Amount")
    spending_category=SelectField("Spending Category",coerce=int,validate_choice=False)
    payment_method=SelectField("Payment Method", coerce=int,validate_choice=False)
    receipt_image=FileField("Reciept Image", validators=[FileAllowed(images,'Images only are allowed (optional) (.jpg, .jpe, .jpeg, .png, .gif, .svg, and .bmp)!')])
    submit = SubmitField("Submit")

class SpendingCategoryForm(FlaskForm):
    name = StringField("Category Name")
    submit = SubmitField("Submit")

class PaymentMethodForm(FlaskForm):
    name = StringField("Payment Method")
    submit = SubmitField("Submit")