from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Generated from python command-line. 'import secrets' 'secrets.token_hex(16). Validate forms from bad stuff
# forms.hidden_tag() in the templates for forms is what gives the forms the validation. Very important and needed
app.config['SECRET_KEY'] = '6caa3f03282327a84f0fba47b592b775'
# '///' just means it's a relative path from the current directory. Will create in the 'JD-Book-Blog' dir
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Doing this here after initial setup to prevent circular imports
from flaskblog import routes
