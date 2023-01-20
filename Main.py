import pandas as pd
from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet

app = Flask(__name__, template_folder='templates')
app.config['SERVER_NAME'] = None
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def background_thread():
    """Function that updates the data every 10 seconds"""
    while True:
        data = pd.read_csv('data.csv')
        socketio.emit('update_data', {'data': data.to_html()}, namespace='/test')
        eventlet.sleep(10)

@socketio.on('connect', namespace='/test')
def test_connect():
    """When a client connects, start the background thread"""
    socketio.start_background_task(target=background_thread)

if __name__ == '__main__':
    socketio.run(app)