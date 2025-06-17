from flask import Flask
from flask_socketio import SocketIO, send
from yolo_stream import YoloStreamer

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return 'Hello, world!'

# send messages to stream
@socketio.on('message')
def handle_message(msg):
    print(f'Received message: {msg}')
    send(f'Echo: {msg}', broadcast=True)

# :point_down: Callback to emit via WebSocket
def emit_detections(detections):
    print(f"Emitting detections: {detections}")
    socketio.emit("yolo_data", {"detections": detections})

# :spanner: Inject callback into streamer
streamer = YoloStreamer(on_detections=emit_detections)
streamer.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
