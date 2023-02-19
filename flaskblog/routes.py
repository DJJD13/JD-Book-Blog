import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, BookForm
from flaskblog.models import User, Book
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.date_posted.desc()).paginate(page=page, per_page=5)
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


def save_picture(form_picture):
    # Generate random hex for file name, then split the extension from the original name
    # '_' used to 'throw away' variable we won't use
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Gives full path name to picture file name in the profile_pics dir, then save there
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Use Pillow (PIL) to resize image before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/book/new", methods=["GET", "POST"])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data,
                    rating=form.rating.data, content=form.content.data, poster=current_user)
        db.session.add(book)
        db.session.commit()
        flash('Book has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_book.html', title='New Book',
                           form=form, legend='New Book')


@app.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book)


@app.route("/book/<int:book_id>/update", methods=["GET", "POST"])
@login_required
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.poster != current_user:
        abort(403)
    form = BookForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.rating = form.rating.data
        book.content = form.content.data
        db.session.commit()
        flash('Your book has been updated!', 'success')
        return redirect(url_for('book', book_id=book_id))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.rating.data = book.rating
        form.content.data = book.content
    return render_template('create_book.html', title='Update Book',
                           form=form, legend='Update Book')


@app.route("/book/<int:book_id>/delete", methods=["POST"])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.poster != current_user:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('Your book has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_books(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    books = Book.query.filter_by(poster=user)\
        .order_by(Book.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_books.html', books=books, user=user)
