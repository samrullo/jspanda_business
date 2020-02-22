import os
from flask import current_app
from flask_uploads import UploadSet, configure_uploads, IMAGES
import datetime
import logging
import pandas as pd
from flask import flash, url_for
from flask import render_template
from flask import redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SubmitField, HiddenField, DateField, IntegerField, FloatField, TextAreaField, FileField, validators
import boto3
from botocore.exceptions import ClientError
from application.utils.utils import to_yyyymmdd


class Controller:
    def __init__(self):
        self.name = "controller"

    def add(self):
        logging.info("Will add new item")

    def edit(self, id):
        logging.info(f"Will edit record with {id}")

    def remove(self, id):
        logging.info(f"Will remove record with {id}")
