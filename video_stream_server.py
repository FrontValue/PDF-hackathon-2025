import argparse
import logging
import logging.config
import threading

from flask import Flask, Response

import conf
from camera import Camera
from shared_camera import SharedCamera

logging.config.dictConfig(conf.dictConfig)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.after_request
def add_header(r):
	"""
	Add headers to both force latest IE rendering or Chrome Frame,
	and also to cache the rendered page for 10 minutes
	"""
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers["Cache-Control"] = "public, max-age=0"
	return r

def gen(camera):
    logger.debug("Starting stream")
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def entrypoint():
    return Response(gen(camera),
        mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000, help="Running port")
    parser.add_argument('-f', '--fps', type=int, default=60, help="Frames per second")
    parser.add_argument('-H', '--host', type=str, default='0.0.0.0', help="Address to broadcast")
    args = parser.parse_args()

    logger.debug("Starting server")

    # Run camera in background if it's blocking
    camera = Camera(fps=args.fps)

    camera_thread = threading.Thread(target=camera.run)
    camera_thread.start()

    app.run(host=args.host, port=args.port)
