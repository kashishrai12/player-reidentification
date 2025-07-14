import cv2
from ultralytics import YOLO

def detect_players(video_path, model_path, output_path):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    detections = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        for box in results[0].boxes:
            if box.cls == 0:  # Assuming class 0 is player
                detections.append({
                    'frame': frame_idx,
                    'bbox': box.xyxy[0].tolist(),
                    'conf': float(box.conf[0])
                })
        frame_idx += 1

    # Save detections to file
    import json
    with open(output_path, 'w') as f:
        json.dump(detections, f)

if __name__ == "__main__":
    detect_players(
        "../data/15sec_input_720p.mp4",
        "../model/yolov11.pt",
        "../data/detections.json"
    )