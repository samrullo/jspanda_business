from application.auth.auth_model import User, db
from flask import flash, redirect, url_for
from flask import render_template
from application.controllers.controller import Controller


class UserController(Controller):
    def __init__(self):
        super().__init__()
        self.name = "user controller"

    def main(self):
        users = User.query.all()
        return render_template("users_main.html", title="Управление полъзователей", users=users)

    def make_admin(self, id):
        user = User.query.get(id)
        user.is_admin = True
        db.session.commit()
        flash(f"Сделал {user.name}, {user.email} админом", "success")
        return redirect(url_for("users_admin_bp.main"))

    def remove_admin(self, id):
        user = User.query.get(id)
        user.is_admin = False
        db.session.commit()
        flash(f"Удалил {user.name}, {user.email}  из админов", "success")
        return redirect(url_for("users_admin_bp.main"))

    def enable_account(self, id):
        user = User.query.get(id)
        user.is_active = True
        db.session.commit()
        flash(f"Enabled account of {user.login}")
        return redirect(url_for("users_admin_bp.main"))

    def disable_account(self, id):
        user = User.query.get(id)
        user.is_active = False
        db.session.commit()
        flash(f"Disabled account of {user.login}")
        return redirect(url_for("users_admin_bp.main"))
