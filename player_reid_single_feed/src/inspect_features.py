import json
with open("../data/deepsort_tracks_grouped.json") as f:
    tracks = json.load(f)
for t in tracks:
    print(f"Track ID {t['id']} length: {len(t['frames'])}")