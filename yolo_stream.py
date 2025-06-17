import cv2
import torch
import threading
import time
from datetime import datetime
import numpy as np

from camera import Camera

class YoloStreamer:
    def __init__(self, on_detections=None):
        self.model = torch.hub.load('yolov5', 'yolov5n', source='local')
        self.cap = Camera(fps=10)
        self.cap.run()  # Start the camera capture thread

        self.on_detections = on_detections  
        self.running = False
        self.thread = None

    def _run(self):
        while self.running:
            frame = self.cap.get_frame(_bytes=False)
            if frame is None or not isinstance(frame, np.ndarray):
                print("[YOLO] ❌ Invalid frame format.")
                time.sleep(0.1)  # Add small delay to prevent CPU spinning
                continue

            try:
                # Ensure frame is in the correct format (BGR to RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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

            except Exception as e:
                print(f"[YOLO] ❌ Error processing frame: {str(e)}")

            time.sleep(0.5)

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
            self.cap.stop()
            if self.thread:
                self.thread.join()

