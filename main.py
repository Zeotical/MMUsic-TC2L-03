from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chat'

mysql = MySQL(app)
app.config['SECRET_KEY'] = 'chatroom1234'
socketio = SocketIO(app)

def add_text(chatroomID, content):
    try:
        print(f"Attempting to insert message: '{content}' into chatroom: {chatroomID}")
        query = "INSERT INTO messages (chatroomID, content) VALUES (%s, %s)" #insert typed messages to database(chat) table(messages) column(content)
        cur = mysql.connection.cursor()
        cur.execute(query, (chatroomID, content))
        mysql.connection.commit()
        print("Message successfully added.")
    except Exception as e:
        print(f"Error saving message to database: {e}")
    finally:
        cur.close()

@app.route('/', methods=['GET', 'POST'])
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
    cur.execute('SELECT chatroomID, chatroom_name FROM chatroom')
    genres = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('chatroom.html', genres=genres)
    
@app.route('/chatroom/<int:chatroomID>', methods=['GET', 'POST'])
def chat(chatroomID):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # Get the content of the new message from the form (assuming the form has an input with name='content')
        content = request.form.get('content')
        if content:
            add_text(chatroomID, content)
        else:
            print("No 'content' found in form data")
    
    cur.execute("SELECT content FROM messages WHERE chatroomID = %s ORDER BY created_at ASC", (chatroomID,))
    mysql.connection.commit()
    results = cur.fetchall()
    cur.close()
    return render_template('chat.html', results=results, chatroomID=chatroomID)


@socketio.on('joined')
def handle_joined(data):
    chatroomID = data['chatroomID']
    join_room(chatroomID)
    emit('message', {'username': 'System', 'text': 'Welcome to Chatroom'}, room=chatroomID) #send Welcome to Chatroom to all the connected clients.
    
@socketio.on('text')
def handle_text(data):
    text = data['text'] #Extracts the message text from the received data
    chatroomID = data['chatroomID']
    username = 'User'
    
    add_text(chatroomID, text) #Calls add_text() to save the message to the database
    emit('message', {'username': username, 'text': text}, room=chatroomID) #Emits the message to all connected clients
    

if __name__ == "__main__":
    socketio.run(app, debug=True)