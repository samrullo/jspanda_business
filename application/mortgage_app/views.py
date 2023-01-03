import os
from . import mortgage_app_bp
from flask import render_template,current_app
from flask import send_file

@mortgage_app_bp.route("/")
def mortgage_app():
    react_mortgage_app_index_path = current_app.config["REACT_MORTGAGE_APP_FOLDER"]/"build"/"index.html"
    current_app.logger.info(f"absolute path of '../../../react-mortgage-app/build/index.html' is {os.path.abspath('react-mortgage-app/build/index.html')}")
    return render_template("mortgage_index.html")