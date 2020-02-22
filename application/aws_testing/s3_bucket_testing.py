import boto3
import logging
from botocore.exceptions import ClientError
import os
import re

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)

bucket_name = "elasticbeanstalk-ap-south-1-384482548730"

folder = r"C:\Users\amrul\PycharmProjects\tbot_zero\uzjapa"


# data = open(r"C:\Users\amrul\PycharmProjects\tbot_zero\uzjapa\5078_ароматная_девушка_покоряя_роза_уловимым.jpg", 'rb')
# s3.Bucket(bucket_name).put_object(Key='jspanda_photos/test2.jpg', Body=data)

def upload_file(file_name, bucket_name, object_name=None):
    if not object_name:
        object_name = file_name
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name, ExtraArgs={'ACL': 'public-read'})
        return response
    except ClientError as e:
        logging.error(e)
        return False


for file in os.listdir(folder)[:5]:
    if re.match(".*\.jpg$", file):
        print(file)
        res=upload_file(os.path.join(folder, file), bucket_name, "jspanda_photos/" + file)
