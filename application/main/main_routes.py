from flask import Blueprint, render_template

# Blueprint configuration
main_bp = Blueprint('main_bp', __name__, template_folder='templates', static_folder='static')


@main_bp.route('/')
def home():
    return render_template('index.html', title='Main Flask Application Factory Page')


@main_bp.route('/fx')
def fx():
    return render_template("fxcalc.html")
