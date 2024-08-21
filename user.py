#imports
from flask import Flask,render_template,request,redirect, session, url_for 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key="ily"

# Configure SQL Alchmey
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///userinfo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db = SQLAlchemy(app)

# Database Model # a model represents a single row in our db each user has their own model
class user(db.Model):
    # Class Variables
    id = db.Column(db.integer,primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for ("dashboard"))
    return render_template("index.html")



if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
