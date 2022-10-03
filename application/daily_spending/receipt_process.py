import os
import cv2
import pathlib
import logging
from flask import current_app
from flask_uploads import UploadSet
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
import datetime

def save_receipt_image_and_update_spending_db_record(form:FlaskForm,spending,images:UploadSet,db:SQLAlchemy):
    receipt_filename=f"{spending.name.lower()}_{spending.spending_category.name.lower()}_{spending.payment_method.name.lower()}_{datetime.datetime.strftime(spending.spent_at,'%Y%m%d_%H%M%S')}."
    saved_filename=images.save(form.receipt_image.data,name=receipt_filename)
    saved_filename_path=pathlib.Path(current_app.config["UPLOADED_IMAGES_DEST"])/saved_filename
    extracted_receipt_file=extract_receipt_image_as_gray(saved_filename_path)
    extracted_receipt_filename=extracted_receipt_file.name
    os.remove(saved_filename_path)
    current_app.logger.info(f"saved {extracted_receipt_filename}")
    spending.receipt_image=extracted_receipt_filename
    db.session.add(spending)
    db.session.commit()
    current_app.logger.info(f"saved receipt image {spending.receipt_image} for {spending}")

def extract_receipt_image_as_gray(receipt_file:pathlib.Path):
    """
    Extract receipt from the photo and save it as gray image
    """
    # convert image to grayscale
    img_gray=cv2.imread(str(receipt_file), cv2.IMREAD_GRAYSCALE)
    
    # apply thresholding to the image 
    thresh_val_used, thresh_img = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # extract rectangular contours from the image
    contours,hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # save countour areas into a list, to find the countour with the biggest area later
    contr_areas=[cv2.contourArea(contr) for contr in contours]
    
    # the index of the biggest countour area, which is used to access the contour with the biggest area
    contr_area_max_idx = contr_areas.index(max(contr_areas))
    current_app.logger.debug(f"contour with maximum area : {contr_areas[contr_area_max_idx]:,}")
    biggest_contr=contours[contr_area_max_idx]    
    
    # get bounding rectangle parameters (top left x,y coordinates with width and height)
    br_x,br_y,br_w,br_h = cv2.boundingRect(biggest_contr)
    current_app.logger.debug(f"Bounding rectangle parameters of {receipt_file}  x : {br_x}, y : {br_y}, w : {br_w}, h : {br_h}")

    extracted_gray_receipt_img = img_gray[br_y:br_y+br_h,br_x:br_x+br_w]
    folder=receipt_file.parent
    new_filename=f"{receipt_file.stem}_gray{receipt_file.suffix}"
    cv2.imwrite(str(folder/new_filename),extracted_gray_receipt_img)
    return folder/new_filename