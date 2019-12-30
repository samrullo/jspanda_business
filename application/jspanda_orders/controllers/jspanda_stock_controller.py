from application.jspanda_orders.models.jspanda_stock import Stock, db
from application.jspanda_orders.models.product import Product
from application.jspanda_orders.models.category import Category
import datetime
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateField, IntegerField, FloatField, TextAreaField
from wtforms import SelectField
from application.utils.utils import to_yyyymmdd


class StockForm(FlaskForm):
    product = SelectField("Product", choices=[(product.id, product.name) for product in Product.query.all()], render_kw={"class": "form-control"}, coerce=int)
    quantity = IntegerField("Quantity", render_kw={"class": "form-control"})
    submit = SubmitField("Submit", render_kw={"class": "btn btn-lg btn-dark"})


class StockController:
    def __init__(self):
        self.name = "stock controller"

    def main(self):
        # records = Stock.query.all()
        query = """SELECT s.id,p.name product_name,c.name category, p.price, s.quantity,p.extra_info 
        FROM stock s, product p, category c
        WHERE s.product_id=p.id
        and p.category_id=c.id
        """
        stock_df = pd.read_sql(query, db.engine)
        stock_df['amount'] = stock_df['price'] * stock_df['quantity']
        stock_df.sort_values('quantity', inplace=True)
        total_stock_amount = stock_df['amount'].sum()
        return render_template("stock/show_all_accounts.html", title="JSPanda Stock", stock_df=stock_df, total_stock_amount=total_stock_amount)

    def empty_stock(self):
        query = """SELECT s.id,p.name product_name,c.name category, p.price, s.quantity,p.extra_info 
                FROM stock s, product p, category c
                WHERE s.product_id=p.id
                and p.category_id=c.id
                and s.quantity=0
                """
        stock_df = pd.read_sql(query, db.engine)
        stock_df['amount'] = stock_df['price'] * stock_df['quantity']
        stock_df.sort_values('quantity', inplace=True)
        return render_template("stock/show_all_accounts.html", title="JSPanda Empty Stock", stock_df=stock_df, total_stock_amount=stock_df['amount'].sum())

    def show_stock_by_category(self, category_id):
        query = f""" SELECT s.id,p.name product_name,c.name category, p.price, s.quantity,p.extra_info 
                        FROM stock s, product p, category c
                        WHERE s.product_id=p.id
                        and p.category_id=c.id
                        and c.id={category_id}
                        """
        category_df = pd.read_sql(f"SELECT * FROM category WHERE id={category_id}", db.engine)
        if len(category_df) > 0:
            category = category_df['name'].values[0]
        else:
            category = "NOCATEGORY"
        stock_df = pd.read_sql(query, db.engine)
        stock_df['amount'] = stock_df['price'] * stock_df['quantity']
        stock_df.sort_values('quantity', inplace=True)
        total_stock_amount = stock_df['amount'].sum()
        return render_template("stock/show_all_accounts.html", title=f"{category} Stock", stock_df=stock_df, total_stock_amount=total_stock_amount)

    def show_by_category_stock_summary(self):
        query = """SELECT s.id,p.name product_name,c.name category, p.price, s.quantity,p.extra_info 
                       FROM stock s, product p, category c
                       WHERE s.product_id=p.id
                       and p.category_id=c.id                       
                       """
        stock_df = pd.read_sql(query, db.engine)
        stock_df['amount'] = stock_df['price'] * stock_df['quantity']
        total_amount = stock_df['amount'].sum()
        category_stock_df = pd.pivot_table(stock_df, index='category', values=['product_name', 'amount'], aggfunc={'product_name': 'count', 'amount': 'sum'})
        category_df = pd.read_sql("SELECT * FROM category", db.engine)
        by_category_stock_df = pd.merge(left=category_df, right=category_stock_df, left_on='name', right_index=True)
        by_category_stock_df.sort_values('product_name', ascending=False, inplace=True)
        return render_template("jspanda_stock_by_category.html", title="JSPanda By category Stock summary", by_category_stock_df=by_category_stock_df, total_amount=total_amount)

    def add(self):
        form = StockForm()
        if form.validate_on_submit():
            new_record = Stock(product_id=form.product.data, quantity=form.quantity.data)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Added stock for  {new_record.product}, {new_record.quantity}", "success")
            return redirect("/jspanda_stock")
        form.product.choices = [(product.id, product.name) for product in Product.query.all()]
        return render_template("stock/add.html", title="Add new stock", form=form)

    def edit(self, id):
        record = Stock.query.get(id)
        form = StockForm()
        if form.validate_on_submit():
            record.product_id = form.product.data
            record.quantity = form.quantity.data
            db.session.commit()
            flash(f"Updated {record.id} to {record.product}, {record.quantity}", "success")
            return redirect("/jspanda_stock")
        form.product.data = record.product_id
        form.quantity.data = record.quantity
        form.product.choices = [(product.id, product.name) for product in Product.query.all()]
        return render_template("stock/edit.html", title="Edit stock", form=form)

    def remove(self, id):
        record = Stock.query.get(id)
        db.session.delete(record)
        db.session.commit()
        flash(f"Removed stock", "success")
        return redirect("/jspanda_stock")