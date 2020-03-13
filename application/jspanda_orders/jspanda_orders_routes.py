from flask import Blueprint, render_template
from flask_login import login_required
from application.jspanda_orders.controllers.jspanda_orders_controllers import JspandaOrderController
from application.jspanda_orders.controllers.jspanda_category_controller import CategoryController
from application.jspanda_orders.controllers.jspanda_product_controller import ProductController
from application.jspanda_orders.controllers.jspanda_stock_controller import StockController

jspanda_orders_bp = Blueprint('jspanda_orders_bp', __name__, template_folder='templates', static_folder='static')


@jspanda_orders_bp.route("/jspanda_orders_home")
@login_required
def jspanda_orders_home():
    contr = JspandaOrderController()
    return contr.jspanda_orders_home()


@jspanda_orders_bp.route("/jspanda_orders")
@login_required
def jspanda_orders():
    contr = JspandaOrderController()
    return contr.show_jspanda_orders()


@jspanda_orders_bp.route("/jspanda_orders_na_prodaju")
@login_required
def jspanda_orders_na_prodaju():
    contr = JspandaOrderController()
    return contr.show_jspanda_na_prodaju_orders()


@jspanda_orders_bp.route("/jspanda_orders_pod_zakaz")
@login_required
def jspanda_orders_pod_zakaz():
    contr = JspandaOrderController()
    return contr.show_jspanda_pod_zakaz_orders()


@jspanda_orders_bp.route("/jspanda_monthly_orders")
@login_required
def jspanda_monthly_orders():
    contr = JspandaOrderController()
    return contr.show_jspanda_monthly_profit()


@jspanda_orders_bp.route("/jspanda_orders_by_date/<adate>")
@login_required
def jspanda_orders_by_date(adate):
    contr = JspandaOrderController()
    return contr.show_jspanda_orders_by_date(adate)


@jspanda_orders_bp.route("/jspanda_orders_by_date_na_prodaju/<adate>")
@login_required
def jspanda_orders_by_date_na_prodaju(adate):
    contr = JspandaOrderController()
    return contr.show_jspanda_orders_by_date_na_prodaju(adate)


@jspanda_orders_bp.route("/add_jspanda_order/<adate>", methods=['GET', 'POST'])
@login_required
def add_jspanda_order(adate):
    contr = JspandaOrderController()
    return contr.add_jspanda_order(adate)


@jspanda_orders_bp.route("/edit_jspanda_order/<id>", methods=['GET', 'POST'])
@login_required
def edit_jspanda_order(id):
    contr = JspandaOrderController()
    return contr.edit_jspanda_order(id)


@jspanda_orders_bp.route("/remove_jspanda_order/<id>", methods=['GET', 'POST'])
@login_required
def remove_jspanda_order(id):
    contr = JspandaOrderController()
    return contr.remove_jspanda_order(id)


@jspanda_orders_bp.route("/mark_jspanda_order_as_paid_or_nonpaid/<id>", methods=['GET', 'POST'])
@login_required
def mark_jspanda_order_as_paid_or_nonpaid(id):
    contr = JspandaOrderController()
    return contr.mark_as_paid_or_nonpaid(id)


@jspanda_orders_bp.route("/mark_jspanda_orders_as_paid_or_nonpaid_by_date/<adate>", methods=['GET', 'POST'])
@login_required
def mark_jspanda_orders_as_paid_or_nonpaid_by_date(adate):
    contr = JspandaOrderController()
    return contr.mark_as_paid_or_nonpaid_by_date(adate)


@jspanda_orders_bp.route("/mark_jspanda_order_as_received_or_nonreceived/<id>", methods=['GET', 'POST'])
@login_required
def mark_jspanda_order_as_received_or_nonreceived(id):
    contr = JspandaOrderController()
    return contr.mark_as_recived_or_nonreceived(id)


@jspanda_orders_bp.route("/mark_as_yubin_received_or_nonreceived/<id>")
@login_required
def mark_as_yubin_received_or_nonreceived(id):
    contr = JspandaOrderController()
    return contr.mark_as_yubin_received_or_nonreceived(id)


@jspanda_orders_bp.route("/mark_jspanda_orders_as_received_by_date/<adate>")
@login_required
def mark_jspanda_orders_as_received_by_date(adate):
    contr = JspandaOrderController()
    return contr.mark_as_received_by_date(adate)


# routes for category
@jspanda_orders_bp.route("/jspanda_category")
@login_required
def jspanda_category():
    contr = CategoryController()
    return contr.main()


@jspanda_orders_bp.route("/add_jspanda_category", methods=['GET', 'POST'])
@login_required
def add_jspanda_category():
    contr = CategoryController()
    return contr.add()


@jspanda_orders_bp.route("/edit_jspanda_category/<id>", methods=['GET', 'POST'])
@login_required
def edit_jspanda_category(id):
    contr = CategoryController()
    return contr.edit(id)


@jspanda_orders_bp.route("/remove_jspanda_category/<id>", methods=['GET', 'POST'])
@login_required
def remove_jspanda_category(id):
    contr = CategoryController()
    return contr.remove(id)


# routes for products
@jspanda_orders_bp.route("/jspanda_product")
@login_required
def jspanda_product():
    contr = ProductController()
    return contr.main()


@jspanda_orders_bp.route("/add_jspanda_product", methods=['GET', 'POST'])
@login_required
def add_jspanda_product():
    contr = ProductController()
    return contr.add()


@jspanda_orders_bp.route("/edit_jspanda_product/<id>", methods=['GET', 'POST'])
@login_required
def edit_jspanda_product(id):
    contr = ProductController()
    return contr.edit(id)


@jspanda_orders_bp.route("/remove_jspanda_product/<id>", methods=['GET', 'POST'])
@login_required
def remove_jspanda_product(id):
    contr = ProductController()
    return contr.remove(id)


# routes for stock
@jspanda_orders_bp.route("/jspanda_stock")
@login_required
def jspanda_stock():
    contr = StockController()
    return contr.main()


@jspanda_orders_bp.route("/jspanda_empty_stock")
@login_required
def jspanda_empty_stock():
    contr = StockController()
    return contr.empty_stock()


@jspanda_orders_bp.route("/jspanda_stock_by_category_summary")
@login_required
def jspanda_stock_by_category_summary():
    contr = StockController()
    return contr.show_by_category_stock_summary()


@jspanda_orders_bp.route("/jspanda_stock_by_category/<category_id>")
@login_required
def jspanda_stock_by_category(category_id):
    contr = StockController()
    return contr.show_stock_by_category(category_id)


@jspanda_orders_bp.route("/add_jspanda_stock", methods=['GET', 'POST'])
@login_required
def add_jspanda_stock():
    contr = StockController()
    return contr.add()


@jspanda_orders_bp.route("/edit_jspanda_stock/<id>", methods=['GET', 'POST'])
@login_required
def edit_jspanda_stock(id):
    contr = StockController()
    return contr.edit(id)


@jspanda_orders_bp.route("/remove_jspanda_stock/<id>", methods=['GET', 'POST'])
@login_required
def remove_jspanda_stock(id):
    contr = StockController()
    return contr.remove(id)


# route for jspanda stock dashboard
@jspanda_orders_bp.route("/jspanda_stock_dashboard")
@login_required
def jspanda_stock_dashboard():
    return render_template("jspanda_stock_dashboard.html", title="Jspanda Stock dashboard")
