import os


class Config:
    TESTING = os.environ.get('TESTING')
    DEBUG = os.environ.get('DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xdf_4\xb0\xbePt\xaaN;\xeb\x9cE\xfd\x0e;\xc8\xb5*{\xa2\x10\x11'

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql://samrullo:18Aranid@aa1dg95lku49n8o.crrz64gldft9.ap-south-1.rds.amazonaws.com/jspanda'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')