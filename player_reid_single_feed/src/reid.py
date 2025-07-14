import cv2
import json
import numpy as np

def extract_appearance_features(video_path, tracks, detections):
    cap = cv2.VideoCapture(video_path)
    features = {}
    for track in tracks:
        for frame_idx, centroid in zip(track['frames'], track['centroids']):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                continue
            # Find detection bbox for this centroid
            for det in detections:
                if det['frame'] == frame_idx:
                    bbox = det['bbox']
                    x1, y1, x2, y2 = map(int, bbox)
                    crop = frame[y1:y2, x1:x2]
                    hist = cv2.calcHist([crop], [0, 1, 2], None, [8, 8, 8],
                                        [0, 256, 0, 256, 0, 256])
                    hist = cv2.normalize(hist, hist).flatten()
                    features.setdefault(track['id'], []).append(hist)
    # Average features per track
    avg_features = {tid: np.mean(f, axis=0) for tid, f in features.items()}
    return avg_features

if __name__ == "__main__":
    with open("../data/tracks_merged.json") as f:
        tracks = json.load(f)
    with open("../data/detections.json") as f:
        detections = json.load(f)
    features = extract_appearance_features("../data/15sec_input_720p.mp4", tracks, detections)
    # Save features for further matching/re-id
    np.save("../data/features_merged.npy", features)