import os


class Config:
    # Generated from python command-line. 'import secrets' 'secrets.token_hex(16)' Validate forms from bad stuff
    # forms.hidden_tag() in the templates for forms is what gives the forms the validation. Very important and needed
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # '///' just means it's a relative path from the current directory. Will create in the 'JD-Book-Blog' dir
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # Need to set these on Macbook. Using an app password for 2-factor bypass
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
