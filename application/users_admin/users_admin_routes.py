from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from application.utils.utils import admin_required
from application.users_admin.controllers.users_controller import UserController

# Blueprint configuration
users_admin_bp = Blueprint('users_admin_bp', __name__, template_folder='templates', static_folder='static', url_prefix="/admin")


@users_admin_bp.route('/users_admin')
@login_required
@admin_required
def main():
    contr = UserController()
    return contr.main()


@users_admin_bp.route("/make_admin/<id>")
@login_required
@admin_required
def make_admin(id):
    contr = UserController()
    return contr.make_admin(id)


@users_admin_bp.route("/remove_admin/<id>")
@login_required
@admin_required
def remove_admin(id):
    contr = UserController()
    return contr.remove_admin(id)


@users_admin_bp.route("/enable_user/<id>")
@login_required
@admin_required
def enable_user(id):
    contr = UserController()
    return contr.enable_account(id)


@users_admin_bp.route("/disable_user/<id>")
@login_required
@admin_required
def disable_user(id):
    contr = UserController()
    return contr.disable_account(id)
