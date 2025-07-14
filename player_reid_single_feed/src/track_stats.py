import json
import numpy as np
from collections import Counter

N = 10  # Threshold for "long" tracks

with open("../data/deepsort_tracks_grouped_interpolated.json") as f:
    tracks = json.load(f)

# Track lengths
lengths = [len(t["frames"]) for t in tracks]
avg_len = np.mean(lengths)
median_len = np.median(lengths)
long_tracks = sum(l > N for l in lengths)

# Tracks per frame
frame_counts = Counter()
for t in tracks:
    for f in t["frames"]:
        frame_counts[f] += 1
avg_tracks_per_frame = np.mean(list(frame_counts.values()))

# Average step per track (smoothness)
avg_steps = []
for t in tracks:
    centroids = np.array(t["centroids"])
    if len(centroids) > 1:
        dists = np.linalg.norm(centroids[1:] - centroids[:-1], axis=1)
        avg_steps.append(np.mean(dists))
if avg_steps:
    avg_step_per_track = np.mean(avg_steps)
else:
    avg_step_per_track = 0

# Reporting
print("=== Tracking Statistics ===")
print(f"Total tracks: {len(tracks)}")
print(f"Average track length: {avg_len:.2f} frames")
print(f"Median track length: {median_len:.2f} frames")
print(f"Tracks longer than {N} frames: {long_tracks}")
print(f"Average tracks per frame: {avg_tracks_per_frame:.2f}")
print(f"Average centroid step per track: {avg_step_per_track:.2f} pixels")