from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Book

books = [
    {
        'title': 'Moby Dick',
        'author': 'Herman Melville',
        'rating': '5/5',
        'content': 'My favorite book',
        'poster': 'JD Eggert',
        # 'date_started': 'March 15th, 2020',
        # 'date_finished': 'April 15th, 2020',
        'date_posted': 'April 20th, 2020'
    },
    {
        'title': 'Pride & Prejudice',
        'author': 'Jane Austin',
        'rating': '5/5',
        'content': 'Another favorite book',
        'poster': 'Domenic Egger',
        # 'date_started': 'March 18th, 2020',
        # 'date_finished': 'April 19th, 2020',
        'date_posted': 'April 22nd, 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', books=books)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


# 'methods' argument allows methods to that page (GET, POST, etc.)
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
