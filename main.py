from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def chat():
    return render_template('chat.html')

@socketio.on('joined')
def handle_joined(data):
    emit('message', {'username': 'System', 'text': 'Welcome to Music Chat'}, broadcast=True)
    
@socketio.on('text')
def handle_text(data):
    text = data['text']
    username = 'User'
    emit('message', {'username': username, 'text': text}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)