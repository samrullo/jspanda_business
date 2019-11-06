import os


class Config:
    TESTING = os.environ.get('TESTING')
    DEBUG = os.environ.get('DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xdf_4\xb0\xbePt\xaaN;\xeb\x9cE\xfd\x0e;\xc8\xb5*{\xa2\x10\x11'

    SQLALCHEMY_DATABASE_URI = 'mysql://samrullo:18Aranid@jspandabusiness.crrz64gldft9.ap-south-1.rds.amazonaws.com/jspanda' or os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
