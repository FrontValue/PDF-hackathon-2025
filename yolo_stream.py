import cv2
import torch
import threading
import time
from datetime import datetime

class YoloStreamer:
    def __init__(self, socketio=None, cam_index=0):
        self.model = torch.hub.load('yolov5', 'yolov5n', source='local')
        self.cap = cv2.VideoCapture(cam_index)
        self.socketio = socketio  # Optional
        self.running = False
        self.thread = None

    def _run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("[YOLO] ❌ Failed to read frame.")
                continue

            results = self.model(frame)
            df = results.pandas().xyxy[0][['name', 'confidence']]
            detections = df.to_dict(orient='records')

            timestamp = datetime.now().strftime('%H:%M:%S')
            if not df.empty:
                print(f"[{timestamp}] Detections:\n{df}")
            else:
                print(f"[{timestamp}] No detections.")

            if self.socketio:
                self.socketio.emit('yolo_data', {'detections': detections})

            time.sleep(0.5)

        self.cap.release()

    def start(self):
        if not self.running:
            print("[YOLO] 🔄 Starting stream...")
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def stop(self):
        if self.running:
            print("[YOLO] 🛑 Stopping stream...")
            self.running = False
            self.thread.join()

if __name__ == "__main__":
    streamer = YoloStreamer()
    try:
        streamer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        streamer.stop()

