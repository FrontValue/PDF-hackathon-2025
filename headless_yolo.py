import cv2
import torch
import datetime

# Load YOLOv5 model (make sure yolov5 is cloned locally and hubconf.py exists)
model = torch.hub.load('yolov5', 'yolov5n', source='local')
model.eval()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("❌ Could not open webcam")

frame_count = 0

while frame_count < 5:  # Just process 5 frames for testing
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture frame")
        break

    results = model(frame)

    print(f"\n[Frame {frame_count}]")
    print(results.pandas().xyxy[0][['name', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']])

    # # # Save annotated frame
    # annotated_frame = results.render()[0]
    # cv2.imwrite(f"output_frame_{frame_count}.jpg", annotated_frame)

    # Generate a timestamp string like: 2025-06-17_15-30-45
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    annotated_frame = results.render()[0]
    cv2.imwrite(f"images/{timestamp}_output_frame_{frame_count}.jpg", annotated_frame)

    frame_count += 1

cap.release()
