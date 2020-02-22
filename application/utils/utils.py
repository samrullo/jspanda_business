import datetime
import logging
from functools import wraps
from flask import request, current_app, flash, redirect, url_for
from flask_login import current_user

to_yyyymmdd = lambda x: datetime.datetime.strftime(x, '%Y%m%d')


def get_logger():
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    return logging.getLogger(__file__)


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in ['OPTIONS']:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin:
            flash("Так как вы не администратор, вход запрешён", "danger")
            return redirect(url_for("main_bp.home"))
        return func(*args, **kwargs)

    return decorated_view
