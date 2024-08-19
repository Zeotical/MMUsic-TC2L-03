#imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#My app
app= Flask(__name__)


@app.route("/")
def index():
    return"Testing 123"

if __name__ in "__main__":
    app.run(debug=True)