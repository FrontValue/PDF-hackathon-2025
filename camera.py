import cv2
import threading
import time
import logging
import os
from logging.handlers import RotatingFileHandler
import numpy as np

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
logger = logging.getLogger(__name__)

# Add file handler for camera.py
file_handler = RotatingFileHandler('logs/camera.log', maxBytes=1024 * 1024, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

thread = None

class Camera:
	def __init__(self,fps=20,video_source=0):
		logger.info(f"Initializing camera class with {fps} fps and video_source={video_source}")
		self.fps = fps
		self.video_source = video_source
		self.camera = None
		self.initialize_camera()
		# We want a max of 5s history to be stored, thats 5s*fps
		self.max_frames = 5*self.fps
		self.frames = []
		self.isrunning = False

	def initialize_camera(self):
		try:
			self.camera = cv2.VideoCapture(self.video_source)
			if not self.camera.isOpened():
				logger.error(f"Failed to open camera at index {self.video_source}")
				# Try alternative camera indices
				for i in range(1, 5):  # Try indices 1-4
					self.camera = cv2.VideoCapture(i)
					if self.camera.isOpened():
						logger.info(f"Successfully opened camera at index {i}")
						self.video_source = i
						break
				if not self.camera.isOpened():
					raise Exception("No camera found")
		except Exception as e:
			logger.error(f"Error initializing camera: {str(e)}")
			self.camera = None

	def run(self):
		if self.camera is None:
			logger.error("Cannot start camera thread: No camera available")
			return

		logging.debug("Preparing thread")
		global thread
		if thread is None:
			logging.debug("Creating thread")
			thread = threading.Thread(target=self._capture_loop,daemon=True)
			logger.debug("Starting thread")
			self.isrunning = True
			thread.start()
			logger.info("Thread started")

	def _capture_loop(self):
		if self.camera is None:
			logger.error("Cannot start capture loop: No camera available")
			return

		dt = 1/self.fps
		logger.debug("Observation started")
		while self.isrunning:
			try:
				v,im = self.camera.read()
				if v:
					if len(self.frames)==self.max_frames:
						self.frames = self.frames[1:]
					self.frames.append(im)
				else:
					logger.warning("Failed to read frame from camera")
			except Exception as e:
				logger.error(f"Error in capture loop: {str(e)}")
			time.sleep(dt)
		logger.info("Thread stopped successfully")

	def stop(self):
		logger.debug("Stopping thread")
		self.isrunning = False
		if self.camera is not None:
			self.camera.release()

	def get_frame(self, _bytes=True):
		if len(self.frames) > 0:
			if _bytes:
				img = cv2.imencode('.png', self.frames[-1])[1].tobytes()
			else:
				img = self.frames[-1]
		else:
			logger.warning("No frames available in buffer")
			if _bytes:
				img = None
			else:
				img = np.zeros((480, 640, 3), dtype=np.uint8)  # Return a black frame
		return img
		
