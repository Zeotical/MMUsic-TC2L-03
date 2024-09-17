from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, emit, join_room
from flask_mysqldb import MySQL
import secrets

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chat'

mysql = MySQL(app)
app.config['SECRET_KEY'] = 'chatroom1234'
socketio = SocketIO(app)

def validate_chatroomID(chatroomID):
    try: 
        cur = mysql.connection.cursor()
        cur.execute("SELECT chatroomID FROM chatroom WHERE chatroomID = %s", (chatroomID,))
        result = cur.fetchone()
        cur.close()
        return result is not None
    except Exception as e:
        print(f"Database error: {e}")
        return False

def save_message(content, chatroomID, user_id):
    if validate_chatroomID(chatroomID):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO messages (content, chatroomID, user_id) VALUES (%s, %s, %s)", (content, chatroomID, user_id))
        mysql.connection.commit()
        cur.close()
        return True
    else:
        print(f"Error: ChatroomID {chatroomID} does not exist")
        return False
    
def get_messages(chatroomID):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT content, created_at, user_id FROM messages WHERE chatroomID = %s ORDER BY created_at ASC", (chatroomID,))
        messages = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return messages
    except Exception as e:
        print(f"Database error: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def chatroom():
    if 'user_id' not in session:
        session['user_id'] = secrets.token_hex(16)
        
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        selected_genre = request.form.get('genre')
        cur.execute('SELECT chatroomID FROM chatroom WHERE chatroomID = %s', (selected_genre,))
        chatroom = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if chatroom:
            return redirect(url_for('chat', chatroomID=chatroom[0]))
    cur.execute('SELECT chatroomID FROM chatroom')
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
        # Get the content of the new message from the form (assuming the form has an input with name='content')
        content = request.form.get('content')
        if content:
            if save_message(content, chatroomID, user_id):
                return jsonify({"status": "success"})
            else:
                return jsonify({"status": "error", "message": "Failed to save message"}), 400
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT background_url FROM chatroom WHERE chatroomID = %s", (chatroomID,))
    background_url = cur.fetchone()[0]  # Fetch the background URL
    print(f"Background URL: {background_url}")
    mysql.connection.commit()
    cur.close()
    
    messages = get_messages(chatroomID)
    return render_template('chat.html', messages=messages, chatroomID=chatroomID, user_id=user_id, background_url=background_url)


@socketio.on('joined')
def handle_joined(data):
    chatroomID = data['chatroomID']
    join_room(chatroomID)
    emit('message', {'username': 'System', 'text': 'Welcome to Chatroom'}, room=chatroomID) #send Welcome to Chatroom to all the connected clients.
    
@socketio.on('text')
def handle_text(data):
    text = data['text'] #Extracts the message text from the received data
    chatroomID = data['chatroomID']
    user_id = "User"
    save_message(text, chatroomID, user_id)
    emit('message', {'username': user_id, 'text': text}, room=chatroomID)#Emits the message to all connected clients
    
@app.route('/livesearch', methods=['POST'])
def livesearch():
    search_text = request.form.get('query', '')
    cursor = mysql.connection.cursor()
    if search_text:
        query = """
        SELECT performer, title, songs_file_name FROM songs 
        WHERE performer LIKE %s OR title LIKE %s
        ORDER BY title ASC LIMIT 10
        """
        search_pattern = f"%{search_text}%"
        cursor.execute(query, (search_pattern, search_pattern))
        search_results = cursor.fetchall()
    else:
        search_results = []
    cursor.close()
    return jsonify(search_results)

if __name__ == "__main__":
    socketio.run(app, debug=True)