import json
import numpy as np
from scipy.optimize import linear_sum_assignment

def load_detections(path):
    with open(path, 'r') as f:
        return json.load(f)

def simple_tracker(detections, max_distance=50):
    tracks = []
    next_id = 0
    prev_centroids = []

    for frame in range(max(d['frame'] for d in detections) + 1):
        frame_dets = [d for d in detections if d['frame'] == frame]
        centroids = [((d['bbox'][0]+d['bbox'][2])/2, (d['bbox'][1]+d['bbox'][3])/2) for d in frame_dets]
        if not centroids:
            prev_centroids = []
            continue  # Skip frames with no detections
        if not prev_centroids:
            # First frame or previous frame had no detections: assign new IDs
            for c in centroids:
                tracks.append({'id': next_id, 'frames': [frame], 'centroids': [c]})
                next_id += 1
        else:
            # Match to previous centroids
            cost = np.linalg.norm(np.array(prev_centroids)[:, None] - np.array(centroids)[None, :], axis=2)
            row_ind, col_ind = linear_sum_assignment(cost)
            assigned = set()
            for r, c in zip(row_ind, col_ind):
                if cost[r, c] < max_distance:
                    tracks[r]['frames'].append(frame)
                    tracks[r]['centroids'].append(centroids[c])
                    assigned.add(c)
            # New detections
            for i, c in enumerate(centroids):
                if i not in assigned:
                    tracks.append({'id': next_id, 'frames': [frame], 'centroids': [c]})
                    next_id += 1
        prev_centroids = centroids
    return tracks

if __name__ == "__main__":
    detections = load_detections("../data/detections.json")
    tracks = simple_tracker(detections)
    with open("../data/tracks.json", "w") as f:
        json.dump(tracks, f)