from application import create_app, db
from application.jspanda_orders.models.category import Category
from application.jspanda_orders.models.product import Product
from application.jspanda_orders.models.jspanda_order import JspandaOrder
from application.jspanda_orders.models.jspanda_stock import Stock

import logging
from flask_migrate import Migrate

_logger = logging.getLogger(__name__)
logging.basicConfig()
_logger.setLevel(logging.INFO)

app = create_app()
migrate = Migrate(app, db)


@app.cli.command("create_db")
def create_db():
    db.create_all()


@app.cli.command("drop_db")
def drop_db():
    db.drop_all()


if __name__ == '__main__':
    _logger.info("Let the show start...")
    app.run()
