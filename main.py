from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chat'

mysql = MySQL(app)
app.config['SECRET_KEY'] = 'chatroom1234'
socketio = SocketIO(app)

def add_text(content):
    query = "INSERT INTO messages (content) VALUES (%s);" #insert typed messages to database(chat) table(messages) column(content)
    cur = mysql.connection.cursor()
    cur.execute(query, (content,))
    mysql.connection.commit()
    cur.close()

@app.route('/', methods=['GET', 'POST'])
def chat():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM messages")
    mysql.connection.commit()
    results = cur.fetchall()
    cur.close()
    return render_template('chat.html', results=results)


@socketio.on('joined')
def handle_joined(data):
    emit('message', {'username': 'System', 'text': 'Welcome to MMusic Chat'}, broadcast=True) #send Welcome to MMUsic Chat to all the connected clients.
    
@socketio.on('text')
def handle_text(data):
    text = data['text'] #Extracts the message text from the received data
    username = 'User'
    add_text(text) #Calls add_text() to save the message to the database
    emit('message', {'username': username, 'text': text}, broadcast=True) #Emits the message to all connected clients
    

if __name__ == "__main__":
    socketio.run(app, debug=True)