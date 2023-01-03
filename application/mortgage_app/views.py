import os
from . import mortgage_app_bp
from flask import render_template,current_app
from flask import send_file

@mortgage_app_bp.route("/")
def mortgage_app():    
    return render_template("mortgage_index.html")