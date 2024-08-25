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

@app.route('/', methods=['GET', 'POST'])
def chat():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Lyrics FROM songs WHERE Lyrics = %s")
    mysql.connection.commit()
    fetchdata = cur.fetchall()
    cur.close()
    if request.method == "POST":
        message = request.form['message']
        if message:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO message (content) VALUES (%s)" , (message,))
            mysql.connection.commit()
    try:
        cur.execute("SELECT * FROM messages")
        mysql.connection.commit()
        messages = cur.fetchall()
    except Exception as e:
        print(f"Error fetching messages: {e}")
        
    cur.close()
    return render_template('chat.html', data=fetchdata)

@socketio.on('joined')
def handle_joined(data):
    emit('message', {'username': 'System', 'text': 'Welcome to MMusic Chat'}, broadcast=True)
    
@socketio.on('text')
def handle_text(data):
    text = data['text']
    username = 'User'
    emit('message', {'username': username, 'text': text}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)