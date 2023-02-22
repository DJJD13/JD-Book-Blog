from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required

from flaskblog import db
from flaskblog.books.forms import BookForm
from flaskblog.models import Book

books = Blueprint('books', __name__)


# 'methods' argument allows methods to that page (GET, POST, etc.)
@books.route("/book/new", methods=["GET", "POST"])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data,
                    rating=form.rating.data, content=form.content.data, poster=current_user)
        db.session.add(book)
        db.session.commit()
        flash('Book has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_book.html', title='New Book',
                           form=form, legend='New Book')


@books.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book)


@books.route("/book/<int:book_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for('books.book', book_id=book_id))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.rating.data = book.rating
        form.content.data = book.content
    return render_template('create_book.html', title='Update Book',
                           form=form, legend='Update Book')


@books.route("/book/<int:book_id>/delete", methods=["POST"])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.poster != current_user:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('Your book has been deleted!', 'success')
    return redirect(url_for('main.home'))
