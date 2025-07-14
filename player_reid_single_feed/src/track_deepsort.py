import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'  # Add this line first

import json
from deep_sort_realtime.deepsort_tracker import DeepSort
import numpy as np
import cv2

# Load detections
with open("../data/detections_filtered.json") as f:
    detections = json.load(f)

# Prepare detections per frame
frames = {}
for d in detections:
    frames.setdefault(d['frame'], []).append({
        'bbox': d['bbox'],
        'confidence': d['conf']
    })

tracker = DeepSort(
    max_age=80,           # Tracks live longer without detection (default 30)
    n_init=2,             # Fewer detections needed to confirm a track (default 3)
    max_iou_distance=0.95  # Allow more flexible association (default 0.7)
)
all_tracks = []

# Open video
cap = cv2.VideoCapture("../data/15sec_input_720p.mp4")
max_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

for frame_idx in range(max_frame):
    ret, frame = cap.read()
    if not ret:
        break

    # Get detections for this frame and format them correctly
    raw_dets = frames.get(frame_idx, [])
    detections_for_tracker = []
    
    for det in raw_dets:
        # Format each detection as [bbox, confidence]
        bbox = det['bbox']  # Should be [x1, y1, x2, y2]
        confidence = det['confidence']
        detections_for_tracker.append([bbox, confidence])

    # Update tracker
    tracks = tracker.update_tracks(detections_for_tracker, frame=frame)

    for t in tracks:
        if not t.is_confirmed():
            continue
        track_id = t.track_id
        ltrb = t.to_ltrb()
        centroid = [(ltrb[0]+ltrb[2])/2, (ltrb[1]+ltrb[3])/2]
        all_tracks.append({
            "frame": frame_idx,
            "id": int(track_id),
            "centroid": centroid,
            "bbox": [float(ltrb[0]), float(ltrb[1]), float(ltrb[2]), float(ltrb[3])]
        })

cap.release()

with open("../data/deepsort_tracks.json", "w") as f:
    json.dump(all_tracks, f, indent=2)