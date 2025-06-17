import cv2
import threading

class SharedCamera:
    def __init__(self, cam_index=0):
        self.cap = cv2.VideoCapture(cam_index)
        self.frame = None
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._read_loop, daemon=True).start()

    def _read_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def get_frame(self):
        return self.frame

    def stop(self):
        self.running = False
        self.cap.release()

