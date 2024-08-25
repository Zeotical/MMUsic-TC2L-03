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
    query = "INSERT INTO messages (content) VALUES (%s);"
    cur = mysql.connection.cursor()
    cur.execute(query, (content,))
    mysql.connection.commit()
    cur.close()

@app.route('/', methods=['GET', 'POST'])
def chat():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Lyrics FROM songs")
    mysql.connection.commit()
    fetchdata = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM messages")
    mysql.connection.commit()
    results = cur.fetchall()
    cur.close()
    return render_template('chat.html', data=fetchdata, results=results)


@socketio.on('joined')
def handle_joined(data):
    emit('message', {'username': 'System', 'text': 'Welcome to MMusic Chat'}, broadcast=True)
    
@socketio.on('text')
def handle_text(data):
    text = data['text']
    username = 'User'
    add_text(text)
    emit('message', {'username': username, 'text': text}, broadcast=True)
    

if __name__ == "__main__":
    socketio.run(app, debug=True)