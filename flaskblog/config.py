import os


class Config:
    SECRET_KEY = os.environ.get('FLASKBLOG_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASKBLOG_DEV_DB_URI')  # /// represents relative path to the current directory
    # Sending mail for password reset
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
