#imports
from flask import Flask,render_template,request,redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import secrets
import os
# from flask_login import LoginManager

app = Flask(__name__)
app.secret_key="user_authentication11"
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'


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
    password = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(1512), nullable=False)
    image = db.Column(db.String(2000) , nullable=False, default='default.svg')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Music_genres(db.Model):
    __tablename__ = 'Music_genres'
    id = db.Column(db.Integer,primary_key=True)
    music_genres = db.Column(db.Text, nullable=False)


class User_genre(db.Model):
    __tablename__ = 'User_genre'
    id = db.Column(db.Integer,primary_key=True)
    user_id =  db.Column(db.Integer,db.ForeignKey('User.id'),  nullable=False)
    genre_id =  db.Column(db.Integer,db.ForeignKey('Music_genres.id'), nullable=False)
    genre_name = db.Column(db.Text, nullable=True)


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
    image_path= 'default.svg'    

    print(request.form)  # This will print the form data in your console for debugging
    
    if 'pfp-select' in request.files:
        image = request.files['pfp-select']

        # Save the image 
        if image and image.filename != '':
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(image.filename)
            image_path = random_hex + f_ext 
            image.save(os.path.join(app.root_path,  app.config['UPLOAD_FOLDER'], image_path))
            print("image saved")
        # else:
        #     image_path= 'default.svg'    
        #     # image.save(os.path.join(app.root_path,  app.config['UPLOAD_FOLDER'], image_path))


    username = request.form["hidden_username"]
    password = request.form["hidden_password"]
    genres = request.form["hidden_genres"]  # Returns a string like 'hiphop,rb'
    
    genre_list = genres.split(',')  # Converts the string to a list

    user = User.query.filter_by(username=username).first()
   
    if user:
        return render_template("index.html", error="User already here!")
    else:
        new_user = User(username=username, image=image_path, password=password)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        for genre_name in genre_list:
            genre = Music_genres.query.filter_by(music_genres=genre_name).first()
            if genre:
                music = User_genre(genre_name=genre_name, user_id=new_user.id, genre_id=genre.id)
                db.session.add(music)
                db.session.commit()

        
        db.session.commit()
        
    

        session["username"]= username
        return redirect(url_for("dashboard"))
# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
     user = User.query.filter_by(username=session["username"]).first()

     return render_template("dashboard.html", username= session["username"], user=user)
    return redirect(url_for("home"))
# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))



# Profile info
@app.route("/profile", methods=["GET","POST"])
def profile():
        # form = profile_form()
        user = User.query.filter_by(username=session["username"]).first()   
        id = user.id
        update= User.query.get_or_404(id)
        # image = user.image  
        if request.method =="POST":
            update.username = request.form["edit_username"]
            update.password = request.form["edit_password"] 

            # Update pfp
            if request.files["pfp-select"]:
                image = request.files["pfp-select"]
                
                if image and image.filename != '':
                    random_hex = secrets.token_hex(8)
                    _, f_ext = os.path.splitext(image.filename)
                    image_path = random_hex + f_ext 
                    image.save(os.path.join(app.root_path,  app.config['UPLOAD_FOLDER'], image_path))
                    update.image = image_path
                    print("image saved")
            session["username"] = update.username
         
            db.session.commit()

    
        
        return render_template("profile.html" , update=update, user=session["username"])

        # return redirect(url_for("home"))

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


