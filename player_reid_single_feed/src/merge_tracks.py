import json

with open('../data/tracks.json') as f:
    tracks = json.load(f)
with open('../data/merge_candidates.json') as f:
    merge_candidates = json.load(f)

# Convert list of tracks to dict for easy access
track_dict = {track['id']: track for track in tracks}

# Keep track of which IDs have been merged
merged = {}

for id1, id2, sim in merge_candidates:
    if id1 in track_dict and id2 in track_dict:
        # Merge frames and centroids
        track_dict[id1]['frames'] += track_dict[id2]['frames']
        track_dict[id1]['centroids'] += track_dict[id2]['centroids']
        # Remove id2
        del track_dict[id2]
        merged[id2] = id1

# Reassign IDs to keep them consecutive (optional)
new_tracks = []
new_id_map = {}
for new_id, old_track in enumerate(track_dict.values()):
    new_tracks.append({
        'id': new_id,
        'frames': old_track['frames'],
        'centroids': old_track['centroids']
    })
    new_id_map[old_track['id']] = new_id

with open('../data/tracks_merged.json', 'w') as f:
    json.dump(new_tracks, f, indent=2)

print(f"Merged tracks saved to ../data/tracks_merged.json")