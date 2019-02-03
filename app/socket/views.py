from .. import socketio

@socketio.on('my event')
def handle(message):
    print(message)