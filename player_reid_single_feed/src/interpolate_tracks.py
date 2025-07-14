import json

with open("../data/deepsort_tracks_grouped.json") as f:
    tracks = json.load(f)

for t in tracks:
    frames = t["frames"]
    centroids = t["centroids"]
    new_frames = []
    new_centroids = []
    for i in range(len(frames) - 1):
        new_frames.append(frames[i])
        new_centroids.append(centroids[i])
        gap = frames[i + 1] - frames[i]
        if gap > 1 and gap < 10:  # interpolate for short gaps (tune threshold as needed)
            for g in range(1, gap):
                interp = [
                    centroids[i][0] + (centroids[i + 1][0] - centroids[i][0]) * g / gap,
                    centroids[i][1] + (centroids[i + 1][1] - centroids[i][1]) * g / gap
                ]
                new_frames.append(frames[i] + g)
                new_centroids.append(interp)
    new_frames.append(frames[-1])
    new_centroids.append(centroids[-1])
    t["frames"] = new_frames
    t["centroids"] = new_centroids

with open("../data/deepsort_tracks_grouped_interpolated.json", "w") as f:
    json.dump(tracks, f, indent=2)