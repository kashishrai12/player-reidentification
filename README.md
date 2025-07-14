# Player Re-identification & Tracking Pipeline 🎥🔁

## Overview
This repository implements a modular pipeline for **player re-identification (ReID)** and **multi-object tracking (MOT)** across multiple camera feeds.  
You can:
- Detect players using YOLO v1
- Extract appearance features
- Run DeepSORT-based tracking per feed
- Re-identify players across feeds (single + multi-camera)
- Clean, merge, interpolate, and visualize tracks

---

## 🚀 Features

| Stage                     | Description |
|--------------------------|-------------|
| **Detect**               | Use YOLO v1 to detect player bounding boxes. |
| **Extract Appearance**   | Get feature vectors for each detection. |
| **Track (per feed)**     | Use DeepSORT to track players inside a single camera stream. |
| **Merge Tracks**         | Group tracks and resolve ID merges across feeds. |
| **ReID & Interpolation**| Handle missing frames and re-identify players across time and cameras. |
| **Analytics & Visuals**  | Output JSON stats, consolidated track visualizations, and videos. |

---

## 📁 Repository Structure

├── player_reid_single_feed
│ ├── data/
│ │ ├── raw video inputs (.mp4)
│ │ ├── detection & tracking JSONs
│ │ └── visualized track videos
│ ├── model/
│ │ └── yolov11.pt # YOLO v1 weights (large file; not included)
│ ├── src/
│ │ ├── detect.py # runs YOLO inference
│ │ ├── extract_appearance_features.py
│ │ ├── track_deepsort.py
│ │ ├── merge_tracks.py
│ │ ├── interpolate_tracks.py
│ │ └── visualize_tracks.py # creates output videos
│ └── requirements.txt
└── report.md # Project documentation & evaluation
