from application.jspanda_orders.models.product import Product, db
from application.jspanda_orders.models.category import Category
import datetime
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateField, IntegerField, FloatField, TextAreaField
from wtforms import SelectField
from application.utils.utils import to_yyyymmdd

_logger = logging.getLogger(__name__)
logging.basicConfig()
_logger.setLevel(logging.INFO)


class ProductForm(FlaskForm):
    name = StringField("Product name", render_kw={"class": "form-control"})
    category = SelectField("Category", choices=[(category.id, category.name) for category in Category.query.all()], render_kw={"class": "form-control"}, coerce=int)
    price = FloatField("Product price", render_kw={"class": "form-control"})
    extra = StringField("Extra notes", render_kw={"class": "form-control"})
    submit = SubmitField("Submit", render_kw={"class": "btn btn-lg btn-dark"})


class ProductController:
    def __init__(self):
        self.name = "product controller"

    def main(self):
        records = Product.query.all()
        return render_template("product/main.html", title="JSPanda Products", records=records)

    def add(self):
        form = ProductForm()
        if form.validate_on_submit():
            new_record = Product(name=form.name.data, price=form.price.data, extra_info=form.extra.data, category_id=int(form.category.data))
            db.session.add(new_record)
            db.session.commit()
            flash(f"Added product {new_record.name}, {new_record.price},{new_record.extra_info},{new_record.category}", "success")
            return self.main()
        _logger.info(f"Validation not passed yet {form.category.data}")
        form.category.choices = [(category.id, category.name) for category in Category.query.all()]
        return render_template("product/add.html", title="Add new product", form=form)

    def edit(self, id):
        record = Product.query.get(id)
        form = ProductForm()
        if form.validate_on_submit():
            record.name = form.name.data
            record.price = form.price.data
            record.extra_info = form.extra.data
            record.category_id = form.category.data
            db.session.commit()
            flash(f"Updated {record.id} to {record.name}, {record.price}, {record.category},{record.extra_info}", "success")
            return self.main()
        form.name.data = record.name
        form.price.data = record.price
        form.category.data = record.category_id
        form.extra.data = record.extra_info
        form.category.choices = [(category.id, category.name) for category in Category.query.all()]
        return render_template("product/edit.html", title="Edit product", form=form)

    def remove(self, id):
        record = Product.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed product", "success")
        return self.main()
