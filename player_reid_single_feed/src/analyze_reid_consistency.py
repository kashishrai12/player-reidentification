import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

features = np.load('../data/features_merged.npy', allow_pickle=True).item()
with open('../data/tracks_merged.json') as f:
    tracks = json.load(f)

ids = list(features.keys())
threshold = 0.85  # Similarity threshold

for i in range(len(ids)):
    for j in range(i+1, len(ids)):
        sim = cosine_similarity([features[ids[i]]], [features[ids[j]]])[0][0]
        if sim > threshold:
            # Check if their frame ranges overlap
            frames_i = set(tracks[ids[i]]['frames'])
            frames_j = set(tracks[ids[j]]['frames'])
            overlap = frames_i & frames_j
            print(f"IDs {ids[i]} and {ids[j]}: similarity={sim:.3f}, overlap={bool(overlap)}")