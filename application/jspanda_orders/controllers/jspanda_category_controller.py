from application.jspanda_orders.models.category import Category, db
import datetime
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateField, IntegerField, FloatField, TextAreaField
from application.utils.utils import to_yyyymmdd


class CategoryForm(FlaskForm):
    name = StringField("Category name", render_kw={"class": "form-control"})
    submit = SubmitField("Submit", render_kw={"class": "btn btn-lg btn-dark"})


class CategoryController:
    def __init__(self):
        self.name = "category controller"

    def main(self):
        records = Category.query.all()
        return render_template("category/main.html", title="JSPanda Categories", records=records)

    def add(self):
        form = CategoryForm()
        if form.validate_on_submit():
            logging.info(f"Validation occurred successfully to add new category {form.name.data}")
            new_record = Category(name=form.name.data)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Added category {new_record.name}", "success")
            return self.main()
        logging.info(f"New category cvalidation not done yet {form.name.data}")
        return render_template("category/add.html", title="Add new category", form=form)

    def edit(self, id):
        record = Category.query.get(id)
        form = CategoryForm()
        if form.validate_on_submit():
            record.name = form.name.data
            db.session.commit()
            flash(f"Updated {record.id} to {record.name}", "success")
            return self.main()
        form.name.data = record.name
        return render_template("category/edit.html", title="Edit category", form=form)

    def remove(self, id):
        record = Category.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed category")
        return self.main()
