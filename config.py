import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    TESTING = os.environ.get('TESTING')
    DEBUG = os.environ.get('DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xdf_4\xb0\xbePt\xaaN;\xeb\x9cE\xfd\x0e;\xc8\xb5*{\xa2\x10\x11'

    SSL_VALIDATION_FOLDER = os.path.join(basedir, "application/static/ssl_validation_files")

    # SQLALCHEMY_DATABASE_URI = 'mysql://samrullo:18Aranid@jspandabusiness.crrz64gldft9.ap-south-1.rds.amazonaws.com/jspanda' or os.environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = 'mysql://sql12359588:7DcFthZEPG@sql12.freemysqlhosting.net/sql12359588'
    # SQLALCHEMY_DATABASE_URI = 'mysql://samrullo:18Rirezu@68.183.81.44/sql12359588'
    SQLALCHEMY_DATABASE_URI = 'mysql://subkhon:18Rirezu@localhost/sql12359588'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    JSPANDA_STATS_FOLDER = ""

    UPLOADED_PHOTOS_DEST = "static/img"

    GOOGLE_CREDENTIALS_FOLDER = os.path.join(basedir, "credentials")
    GOOGLE_CREDENTIALS_FILE = os.path.join(GOOGLE_CREDENTIALS_FOLDER, "jspanda-abb0ef8b0971.json")
