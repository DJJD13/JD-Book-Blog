# imports from __init__.py in flaskblog
from flaskblog import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
