import json

with open("../data/deepsort_tracks_grouped_interpolated.json") as f:
    tracks = json.load(f)

# Remove short tracks
min_length = 10  # You can adjust this threshold
tracks = [t for t in tracks if len(t["frames"]) >= min_length]

# Placeholder for merging fragmented tracks (advanced, optional)
# For example, you could merge tracks with similar appearance and close in time/space

with open("../data/deepsort_tracks_grouped_cleaned.json", "w") as f:
    json.dump(tracks, f, indent=2)