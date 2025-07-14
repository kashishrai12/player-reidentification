import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

features = np.load('../data/features.npy', allow_pickle=True).item()
with open('../data/tracks.json') as f:
    tracks = json.load(f)

ids = list(features.keys())
threshold = 0.85  # Similarity threshold

merge_candidates = []
for i in range(len(ids)):
    for j in range(i+1, len(ids)):
        sim = cosine_similarity([features[ids[i]]], [features[ids[j]]])[0][0]
        frames_i = set(tracks[ids[i]]['frames'])
        frames_j = set(tracks[ids[j]]['frames'])
        overlap = frames_i & frames_j
        if sim > threshold and overlap:
            merge_candidates.append([int(ids[i]), int(ids[j]), float(sim)])
            print(f"MERGE: IDs {ids[i]} and {ids[j]}: similarity={sim:.3f}, overlap={bool(overlap)}")

# Save for next step
with open('../data/merge_candidates.json', 'w') as f:
    json.dump(merge_candidates, f)