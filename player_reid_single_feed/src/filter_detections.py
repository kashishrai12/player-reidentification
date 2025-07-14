import json

with open("../data/detections.json") as f:
    detections = json.load(f)

# Lower confidence threshold to 0.3
filtered = [d for d in detections if d['conf'] > 0.15]

with open("../data/detections_filtered.json", "w") as f:
    json.dump(filtered, f, indent=2)