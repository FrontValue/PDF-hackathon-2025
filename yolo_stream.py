import cv2
import torch
import threading
import time
from datetime import datetime

from camera import Camera

class YoloStreamer:
    def __init__(self, on_detections=None):
        self.model = torch.hub.load('yolov5', 'yolov5n', source='local')
        self.cap = Camera(fps=10)

        self.on_detections = on_detections  
        self.running = False
        self.thread = None

    def _run(self):
        while self.running:
            ret, frame = self.cap.get_frame()
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

            # 🔁 Send results to callback if defined
            if self.on_detections:
                self.on_detections(detections)

            time.sleep(0.5)

        self.cap.stop()

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
            # self.thread.join()

