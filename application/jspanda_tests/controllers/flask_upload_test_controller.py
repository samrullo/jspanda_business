import os
from flask import current_app
from flask_uploads import UploadSet, configure_uploads, IMAGES
from application.jspanda_orders.models.product import Product, db
from application.jspanda_orders.models.category import Category
import datetime
import logging
import pandas as pd
from flask import flash
from flask import render_template
from flask import redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SubmitField, HiddenField, DateField, IntegerField, FloatField, TextAreaField, FileField, validators
import boto3
from botocore.exceptions import ClientError
from application.utils.utils import to_yyyymmdd

photos = UploadSet('photos', IMAGES)
configure_uploads(current_app, photos)


class UploadForm(FlaskForm):
    photo = FileField("jspanda_image", validators=[FileAllowed(photos, "Images only"), FileRequired('File was empty!')], render_kw={"class": "btn input-group-addon"})
    submit = SubmitField("Submit", render_kw={"class": "btn btn-lg btn-dark"})


class FlaskUploadTestController:
    def __init__(self):
        self.name = "flask upload tester"
        self.bucket_name = "elasticbeanstalk-ap-south-1-384482548730"
        self.bucket_url = "https://elasticbeanstalk-ap-south-1-384482548730.s3.ap-south-1.amazonaws.com"
        self.bucket_folder = "jspanda_photos"

    def upload_file(self, file_name, bucket_name, object_name=None):
        if not object_name:
            object_name = file_name
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket_name, object_name, ExtraArgs={'ACL': 'public-read'})
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload(self):
        form = UploadForm()
        if form.validate_on_submit():
            filename = photos.save(form.photo.data)

            # considering that we saved the file successfully next will attempt to save it to s3 bucket
            if self.upload_file(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename), self.bucket_name, f"{self.bucket_folder}/{filename}"):
                logging.info(f"Successfully saved {os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)} to bucket {self.bucket_url}/{self.bucket_folder}/{filename}")
                file_url = f"{self.bucket_url}/{self.bucket_folder}/{filename}"
                flash(f"Successfully saved {filename} to bucket {file_url}", "success")
            else:
                file_url=None
                flash("Something went wrong", "failure")
        else:
            file_url = None
        return render_template("flask_upload_test_page.html", form=form, file_url=file_url)
