import cv2
import torch

# Load model
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

# Open camera
cap = cv2.VideoCapture(0)

frame_count = 0

while frame_count < 5:  # Process 5 frames then exit
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Inference
    results = model(frame)
    
    # Print to terminal
    print(f"\n[Frame {frame_count}]")
    print(results.pandas().xyxy[0][['name', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']])

    # Optionally save the annotated frame
    annotated = results.render()[0]
    cv2.imwrite(f"output_frame_{frame_count}.jpg", annotated)

    frame_count += 1

cap.release()

