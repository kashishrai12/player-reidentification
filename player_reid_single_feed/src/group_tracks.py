import json
from collections import defaultdict

with open("../data/deepsort_tracks.json") as f:
    tracks = json.load(f)

grouped = defaultdict(lambda: {"id": None, "frames": [], "centroids": []})
for t in tracks:
    tid = t["id"]
    grouped[tid]["id"] = tid
    grouped[tid]["frames"].append(t["frame"])
    grouped[tid]["centroids"].append(t["centroid"])

with open("../data/deepsort_tracks_grouped.json", "w") as f:
    json.dump(list(grouped.values()), f, indent=2)