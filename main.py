#imports
from flask import Flask,render_template,request,redirect, session, url_for, jsonify,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import secrets
import os
from flask_socketio import SocketIO, emit, join_room
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key="user_authentication11"
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'
app.secret_key="user_authentication11"
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chat'
app.config['MYSQL_UNIX_SOCKET'] = '/opt/lampp/var/mysql/mysql.sock'
app.config['MYSQL_UNIX_SOCKET'] = '/opt/lampp/var/mysql/mysql.sock'

mysql = MySQL(app)
app.config['SECRET_KEY'] = 'chatroom1234'
socketio = SocketIO(app)

def validate_chatroomID(chatroomID):
    try: 
        cur = mysql.connection.cursor()
        cur.execute("SELECT chatroomID FROM chatroom WHERE chatroomID = %s", (chatroomID,))
        result = cur.fetchone()
        print(f"Query result: {result}")
        mysql.connection.commit()
        cur.close()
        if result:  # Check if a result was returned
            return True  # Chatroom exists
        else:
            return False
    except Exception as e:
        print(f"Database error: {e}")
        return False

def save_message(content, chatroomID, user_id):
    if validate_chatroomID(chatroomID):
        try:
            cur = mysql.connection.cursor()
            print(f"Inserting message: {content}, ChatroomID: {chatroomID}, UserID: {user_id}")
            cur.execute("INSERT INTO messages (content, chatroomID, user_id) VALUES (%s, %s, %s)", (content, chatroomID, user_id))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Database error while saving message: {e}")
            return False
    else:
        print(f"Error: ChatroomID {chatroomID} does not exist")
        return False

def get_messages(chatroomID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT content, created_at, user_id FROM messages WHERE chatroomID = %s ORDER BY created_at ASC", (chatroomID,))
        messages = cur.fetchall()
        cur.close()
        return messages if messages else []  # Return an empty list if no messages are found
    except Exception as e:
        print(f"Database error: {e}")
        return []


# Configure SQL Alchmey
app.config["SQLALCHEMY_DATABASE_URI"]= "mysql://root:@localhost/chat?unix_socket=/opt/lampp/var/mysql/mysql.sock"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db = SQLAlchemy(app)

# Database Model # a model represents a single row in our db each user has their own model
class user(db.Model):
    # Class Variables
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(1512), nullable=False)
    image = db.Column(db.String(2000) , nullable=True, default='default.svg')
    bio = db.Column(db.String(150), nullable=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class music_genres(db.Model):
    __tablename__ = 'music_genres'
    id = db.Column(db.Integer,primary_key=True)
    music_genre = db.Column(db.Text, nullable=False)


class user_genre(db.Model):
    __tablename__ = 'user_genre'
    id = db.Column(db.Integer,primary_key=True)
    user_id =  db.Column(db.Integer,db.ForeignKey('user.id'),  nullable=False)
    genre_id =  db.Column(db.Integer,db.ForeignKey('music_genres.id'), nullable=False)
    genre_name = db.Column(db.Text, nullable=True)


#Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for ("chatroom"))
    else:
     return render_template("index.html")

# Login
@app.route("/login", methods=["GET","POST"]) #what does this route do what kind of methods are we using- sending/recieving info?
def login():
    #collect into from the form
 if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    users = user.query.filter_by(username=username).first()
    if users and users.check_password (password):
        session["username"] = username
        return redirect(url_for("chatroom"))
    elif users and not users.check_password (password):
        flash('Password does not match records.', 'success')
    else:
        flash('User is not registered, register to proceed.', 'success')

        return render_template("index.html")
 return render_template("login.html")  
    #check if it's in the db/login
    #otherwise show homepage

# Register
@app.route("/register", methods=["POST"])
def register():
    #In case user doesn't add a defaut image.
    image_path= 'default.svg'    
    session["pfp_path"] = image_path
    
    if 'pfp-select' in request.files:
        image = request.files['pfp-select']

        # Save the image 
        if image and image.filename != '':
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(image.filename)
            image_path = random_hex + f_ext 
            image.save(os.path.join(app.root_path,  app.config['UPLOAD_FOLDER'], image_path))
            session["pfp_path"] = image_path

            print("image saved")

    username = request.form["hidden_username"]
    password = request.form["hidden_password"]
    genres = request.form["hidden_genres"]  # Returns a string like 'hiphop,rb'
    
    genre_list = genres.split(',')  # Converts the string to a list

    users = user.query.filter_by(username=username).first()
   
    if users:
        flash('User already exists/Username taken', 'success')
        return render_template("index.html", error="User already here!")
    elif username=="" or password=="":
        flash('Username and password cannot be empty.', 'success')
        return render_template("index.html", error="Empty ps and username!")
    else:
        new_user = user(username=username, image=image_path, password=password)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        for genre_name in genre_list:
            genre = music_genres.query.filter_by(music_genre=genre_name).first()
            if genre:
                music = user_genre(genre_name=genre_name, user_id=new_user.id, genre_id=genre.id)
                db.session.add(music)

        
        db.session.commit()
        
        session["username"]= username
        session["genre_selected"]= genre_list

        return redirect(url_for("chatroom"))

# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

# Profile info
@app.route("/profile", methods=["GET", "POST"])
def profile():
    users = user.query.filter_by(username=session["username"]).first()   
    id = users.id
    update = users.query.get_or_404(id)
    register_genre=user_genre.query.filter_by(user_id=update.id).all()
    genre_list = [genre.genre_name for genre in register_genre]

    if request.method == "POST":
    
        update_username = request.form["edit_username"]
        username_taken = user.query.filter_by(username=update_username).first()  

        
        update.password= request.form["edit_password"] 
       
        if request.form["edit_bio"]:
            update.bio = request.form["edit_bio"]  
            session["bio"]= update.bio
        
        #Check if username is taken
        if username_taken and username_taken.id != update.id:
            flash('Username Taken.', 'success')
            return render_template("profile.html", update=update, user=session["username"], error="Username already exists")  
        update.username= update_username
        #Update pfp
        if request.files["pfp-select"]:
            image = request.files["pfp-select"]
            if image and image.filename != '':
                random_hex = secrets.token_hex(8)
                _, f_ext = os.path.splitext(image.filename)
                image_path = random_hex + f_ext 
                image.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], image_path))
                update.image = image_path
                session["pfp_path"] = image_path
                print("image saved")

        #Update genre selection
        if request.form.get("edit_genre"):
            update.genres = request.form.get("edit_genre")
            genre_list = update.genres.split(',') 
            user_genre.query.filter_by(user_id=update.id).delete()
            for genre_name in genre_list:
                genre = music_genres.query.filter_by(music_genre=genre_name).first()
                if genre:
                    music = user_genre(genre_name=genre_name, user_id=update.id, genre_id=genre.id)
                    db.session.add(music)

            session["genre_selected"] = genre_list
            update.genres = session["genre_selected"]
        else:
            update.genres = session["genre_selected"]

        session["username"] = update.username
        
        db.session.commit()
        flash('Profile updated!', 'success')
    return render_template("profile.html", update=update, user=session["username"],genres=genre_list)


@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        selected_genre = request.form.get('genre')
        cur.execute('SELECT chatroomID FROM chatroom WHERE chatroomID = %s', (selected_genre,))
        chatroom = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if chatroom:
            return redirect(url_for('chatroom', chatroomID=chatroom['chatroomID']))
    cur.execute('SELECT chatroom_name FROM chatroom')
    genres = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('chatroom.html', genres=genres)
    
@app.route('/chatroom/<int:chatroomID>', methods=['GET', 'POST'])
def chat(chatroomID):
    if 'user_id' not in session:
        session['user_id'] = secrets.token_hex(16)

    user_id = session['user_id']
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            if save_message(content, chatroomID, user_id):
                return jsonify({"status": "success"})
            else:
                return jsonify({"status": "error", "message": "Failed to save message"}), 400
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT chatroom_name, background_url FROM chatroom WHERE chatroomID = %s", (chatroomID,))
    chatroom = cur.fetchone()
    cur.close()

    if chatroom:
        chatroom_name = chatroom[0]
        background_url = chatroom[1]
        messages = get_messages(chatroomID)  # Fetch messages safely with the fix
        return render_template('chat.html', room_name=chatroom_name, background=background_url, user_id=user_id, messages=messages)

    return "Chatroom not found", 404



@socketio.on('joined')
def handle_joined(data):
    chatroomID = data['chatroomID']
    join_room(chatroomID)
    emit('message', {'username': 'System', 'text': 'Welcome to Chatroom'}, room=chatroomID) #send Welcome to Chatroom to all the connected clients.
    
@socketio.on('text')
def handle_text(data):
    text = data['text'] #Extracts the message text from the received data
    chatroomID = data['chatroomID']
    username = session["username"]
    pfp = session["pfp_path"]
    
    save_message(text, chatroomID, username) #Calls add_text() to save the message to the database
    emit('message', {'pfp':pfp,'username': username, 'text': text}, room=chatroomID) #Emits the message to all connected clients
    
@app.route('/livesearch', methods=['POST'])
def livesearch():
    search_text = request.form.get('query', '')
    cursor = mysql.connection.cursor()

    genre_selected = session.get('genre_selected')

    if search_text and genre_selected:
        cursor.execute("SELECT id FROM music_genres WHERE music_genre IN %s", (tuple(genre_selected),))
        genre_ids = cursor.fetchall()

        if genre_ids:
            genre_ids = [genre[0] for genre in genre_ids]

            query = """
            SELECT performer, title, lyric, source 
            FROM songs 
            WHERE (performer LIKE %s OR title LIKE %s OR lyric LIKE %s)
            ORDER BY
              CASE
                WHEN genre_id IN %s THEN 1
                ELSE 2
              END,
              title ASC
            LIMIT 10
            """
            
            search_pattern = f"%{search_text}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, tuple(genre_ids)))
            search_results = cursor.fetchall() or []  # Return an empty list if no results are found
        else:
            search_results = []
    else:
        search_results = []

    cursor.close()

    return jsonify(search_results)



if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    # app.run(debug=True)
    socketio.run(app, debug=True)