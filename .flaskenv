FLASK_ENV=development
FLASK_APP=jspanda_business.py
DEBUG=True

SECRET_KEY=b'\xad\n\xf1}\x92\x82\xfd\xaf\x9aodEq\x0fhy\x83\x15\xa2\xf9\x87\xb8\\'
SQLALCHEMY_PSQL_DATABASE_URI='postgresql://samrullo:samrullo@localhost:5432/jspanda'
SQLALCHEMY_MYSQL_DATABASE_URI='mysql+pymysql://samrullo:jspanda@localhost:3306/jspanda'
SQLALCHEMY_DATABASE_URI='postgresql://samrullo:samrullo@localhost:5432/jspanda'
SQLALCHEMY_TRACK_MODIFICATIONS=False