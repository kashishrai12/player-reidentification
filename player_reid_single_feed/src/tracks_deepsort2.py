import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import json
import numpy as np
import cv2
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cosine

# Load detections with appearance features
with open("../data/detections_with_features.json") as f:
    detections = json.load(f)

# Prepare detections per frame
frames = {}
for d in detections:
    frames.setdefault(d['frame'], []).append({
        'bbox': d['bbox'],
        'confidence': d['conf'],
        'appearance_feat': d['appearance_feat']
    })

all_tracks = []
next_id = 0
active_tracks = []

def iou(bbox1, bbox2):
    x1, y1, x2, y2 = bbox1
    x1g, y1g, x2g, y2g = bbox2
    xi1, yi1 = max(x1, x1g), max(y1, y1g)
    xi2, yi2 = min(x2, x2g), min(y2, y2g)
    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    bbox1_area = (x2 - x1) * (y2 - y1)
    bbox2_area = (x2g - x1g) * (y2g - y1g)
    union_area = bbox1_area + bbox2_area - inter_area
    return inter_area / union_area if union_area > 0 else 0

# Open video
cap = cv2.VideoCapture("../data/15sec_input_720p.mp4")
max_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

for frame_idx in range(max_frame):
    ret, frame = cap.read()
    if not ret:
        break

    dets = frames.get(frame_idx, [])
    det_bboxes = [d['bbox'] for d in dets]
    det_feats = [d['appearance_feat'] for d in dets]

    # Prepare track states
    track_bboxes = [tr['bbox'] for tr in active_tracks]
    track_feats = [tr['appearance_feat'] for tr in active_tracks]

    # Association cost: combine IOU and appearance
    if track_bboxes and det_bboxes:
        cost_matrix = np.zeros((len(track_bboxes), len(det_bboxes)))
        for i, (tb, tf) in enumerate(zip(track_bboxes, track_feats)):
            for j, (db, df) in enumerate(zip(det_bboxes, det_feats)):
                iou_score = iou(tb, db)
                app_dist = cosine(tf, df)
                # Lower cost is better: use (1-IOU) + appearance distance
                cost_matrix[i, j] = 0.5 * (1 - iou_score) + 0.5 * app_dist
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        assigned_tracks = set()
        assigned_dets = set()
        # Update matched tracks
        for r, c in zip(row_ind, col_ind):
            if cost_matrix[r, c] < 0.7:  # threshold, tune as needed
                tr = active_tracks[r]
                d = dets[c]
                tr['frames'].append(frame_idx)
                tr['centroids'].append([(d['bbox'][0]+d['bbox'][2])/2, (d['bbox'][1]+d['bbox'][3])/2])
                tr['bbox'] = d['bbox']
                tr['appearance_feat'] = d['appearance_feat']
                all_tracks.append({
                    "frame": frame_idx,
                    "id": tr['id'],
                    "centroid": tr['centroids'][-1],
                    "bbox": d['bbox']
                })
                assigned_tracks.add(r)
                assigned_dets.add(c)
        # Unmatched tracks: keep if not too old (implement max_age if desired)
        active_tracks = [tr for i, tr in enumerate(active_tracks) if i in assigned_tracks]
        # New detections: start new tracks
        for i, d in enumerate(dets):
            if i not in assigned_dets:
                active_tracks.append({
                    'id': next_id,
                    'frames': [frame_idx],
                    'centroids': [[(d['bbox'][0]+d['bbox'][2])/2, (d['bbox'][1]+d['bbox'][3])/2]],
                    'bbox': d['bbox'],
                    'appearance_feat': d['appearance_feat']
                })
                all_tracks.append({
                    "frame": frame_idx,
                    "id": next_id,
                    "centroid": active_tracks[-1]['centroids'][-1],
                    "bbox": d['bbox']
                })
                next_id += 1
    else:
        # No active tracks or no detections: start new tracks for all detections
        for d in dets:
            active_tracks.append({
                'id': next_id,
                'frames': [frame_idx],
                'centroids': [[(d['bbox'][0]+d['bbox'][2])/2, (d['bbox'][1]+d['bbox'][3])/2]],
                'bbox': d['bbox'],
                'appearance_feat': d['appearance_feat']
            })
            all_tracks.append({
                "frame": frame_idx,
                "id": next_id,
                "centroid": active_tracks[-1]['centroids'][-1],
                "bbox": d['bbox']
            })
            next_id += 1

cap.release()

with open("../data/deepsort_tracks.json", "w") as f:
    json.dump(all_tracks, f, indent=2)