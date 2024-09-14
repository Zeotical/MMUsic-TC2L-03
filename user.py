#imports
from flask import Flask,render_template,request,redirect, session, url_for 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

app = Flask(__name__)
app.secret_key="user_authentication11"

#Configure login_manager
# login_manager= LoginManager() #creating an incstance of LoginM
# login_manager.init_app(app)
# @login_manager.user_loader 
# def load_user(user_id):
#     return User.get(user_id)

# Configure SQL Alchmey
app.config["SQLALCHEMY_DATABASE_URI"]= "mysql://root:@localhost/registerdb?unix_socket=/opt/lampp/var/mysql/mysql.sock"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db = SQLAlchemy(app)

# Database Model # a model represents a single row in our db each user has their own model
class User(db.Model):
    # Class Variables
    __tablename__ = 'User'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(1512), nullable=False)
    image = db.Column(db.String(2000) , nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for ("dashboard"))
    else:
     return render_template("index.html")

# Login
@app.route("/login", methods=["GET","POST"]) #what does this route do what kind of methods are we using- sending/recieving info?
def login():
    #collect into from the form
 if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    image = request.form["hidden_image"]

    user = User.query.filter_by(username=username).first()
    if user and user.check_password (password):
        session["username"] = username
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html")
 return render_template("login.html")  
    #check if it's in the db/login
    #otherwise show homepage

# Register
@app.route("/register", methods=["POST"])
def register():
    print(request.form)  # This will print the form data in your console for debugging
    
    # Now fetch the image
    image = request.form.get("hidden_image")
    print(f"Image: {image}")  # Ensure this is not None
    username = request.form["hidden_username"]
    password = request.form["hidden_password"]
    image = request.form["hidden_image"]
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("index.html", error="User already here!")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session["username"]= username
        return redirect(url_for("dashboard"))
# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username= session["username"])
    return redirect(url_for("home"))
# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

# Profile info
@app.route("/profile")
def profile():
    if "username" in session:
        return render_template("profile.html" ,username=session["username"] )
    return redirect(url_for("home"))

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


