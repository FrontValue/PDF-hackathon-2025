import logging
import os
from logging.handlers import RotatingFileHandler
import cv2

from flask import Flask
from flask_socketio import SocketIO, send

from camera import Camera
from yolo_stream import YoloStreamer

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add file handler for app.py
file_handler = RotatingFileHandler('logs/flask.log', maxBytes=1024 * 1024, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return 'Hello, world!'

# send messages to stream
@socketio.on('message')
def handle_message(msg):
    logger.info(f'Received message: {msg}')
    send(f'Echo: {msg}', broadcast=True)


def emit_detections(detections, frame):
    logger.info(f"Emitting detections: {detections}")
    socketio.emit("detections", {"detections": detections})
    
    # Convert frame to bytes if needed (e.g., for transmission)
    # This example assumes JPEG encoding for streaming video frames
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()
    
    socketio.emit("video", {"bytes": frame_bytes}) 

# :spanner: Inject callback into streamer
try:
    streamer = YoloStreamer(on_detections=emit_detections)
    streamer.start()
except Exception as e:
    logger.error(f"Failed to initialize streamer: {e}")

if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
