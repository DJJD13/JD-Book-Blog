from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Book
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
