from flask import Flask, render_template, url_for

app = Flask(__name__)

books = [
    {
        'title': 'Moby Dick',
        'author': 'Herman Melville',
        'rating': '5/5',
        'content': 'My favorite book',
        'poster': 'JD Eggert',
        'date_started': 'March 15th, 2020',
        'date_finished': 'April 15th, 2020',
        'date_posted': 'April 20th, 2020'
    },
    {
        'title': 'Pride & Prejudice',
        'author': 'Jane Austin',
        'rating': '5/5',
        'content': 'Another favorite book',
        'poster': 'Domenic Egger',
        'date_started': 'March 18th, 2020',
        'date_finished': 'April 19th, 2020',
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


if __name__ == "__main__":
    app.run(debug=True)
