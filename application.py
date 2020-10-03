"""
Demo Flask application to test the operation of Flask with socket.io
Aim is to create a webpage that is constantly updated with random numbers from a background python process.
"""
from flask_socketio import SocketIO
from flask import Flask, render_template
from random import random
from threading import Thread, Event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# Turn the flask app into a SocketIO app
socket_io = SocketIO(app, async_mode=None, logger=False, engineio_logger=False)

# Random number Generator Thread
thread = Thread()
thread_stop_event = Event()
thread_counter = 0


def random_number_generator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    while not thread_stop_event.isSet():
        number = round(random() * 10, 3)
        print(number)
        socket_io.emit('new_number', {'number': number}, namespace='/test')
        socket_io.sleep(5)


@app.route('/')
def index():
    # Only by sending this page first the client will be connected to the socket_io instance
    return render_template('index.html')


@socket_io.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    global thread_counter
    thread_counter += 1
    print(f'Clients connected: {thread_counter}')

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread_stop_event.clear()
        thread = socket_io.start_background_task(random_number_generator)


@socket_io.on('disconnect', namespace='/test')
def test_disconnect():
    global thread_counter
    thread_counter -= 1
    print(f'Client disconnected, left: {thread_counter}')
    if thread.is_alive() and thread_counter == 0:
        global thread_stop_event
        thread_stop_event.set()
        print('Disconnected & thread stopped')


if __name__ == '__main__':
    socket_io.run(app)
