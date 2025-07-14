import json
import cv2

with open("../data/deepsort_tracks_grouped.json") as f:
    tracks = json.load(f)

cap = cv2.VideoCapture("../data/15sec_input_720p.mp4")
frame_tracks = {}
for track in tracks:
    tid = track["id"]
    for frame, centroid in zip(track["frames"], track["centroids"]):
        frame_tracks.setdefault(frame, []).append({
            "id": tid,
            "centroid": centroid
        })

# Get video properties for saving
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out_path = "../data/tracks_visualized.mp4"
out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    for t in frame_tracks.get(frame_idx, []):
        cx, cy = map(int, t["centroid"])
        cv2.circle(frame, (cx, cy), 10, (0,255,0), 2)
        cv2.putText(frame, f'ID {t["id"]}', (cx, cy-15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    out.write(frame)
    cv2.imshow("Tracks", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frame_idx += 1

cap.release()
out.release()
cv2.destroyAllWindows()
print(f"Visualization saved to {out_path}")