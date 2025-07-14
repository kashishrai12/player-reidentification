# Player Re-identification & Tracking Pipeline 

## Overview
This repository implements a modular pipeline for **player re-identification (ReID)** and **multi-object tracking (MOT)** across multiple camera feeds.  
You can:
- Detect players using YOLO v1
- Extract appearance features
- Run DeepSORT-based tracking per feed
- Re-identify players across feeds (single + multi-camera)
- Clean, merge, interpolate, and visualize tracks

---

## Features

| Stage                     | Description |
|--------------------------|-------------|
| **Detect**               | Use YOLO v1 to detect player bounding boxes. |
| **Extract Appearance**   | Get feature vectors for each detection. |
| **Track (per feed)**     | Use DeepSORT to track players inside a single camera stream. |
| **Merge Tracks**         | Group tracks and resolve ID merges across feeds. |
| **ReID & Interpolation**| Handle missing frames and re-identify players across time and cameras. |
| **Analytics & Visuals**  | Output JSON stats, consolidated track visualizations, and videos. |

---

## Repository Structure
```
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
```

## Quickstart

1. **Clone the repo**  
   ```bash
   git clone https://github.com/kashishrai12/player-reidentification.git
   cd player-reidentification
   ```

2. **Install dependencies**

```bash
pip install -r player_reid_single_feed/requirements.txt
```

3. Download YOLO weights
```bash
Place your yolov11.pt model file into player_reid_single_feed/model/
If large, host it elsewhere (e.g. Google Drive) and download manually
```

4. **Running Different Approaches**
   ---
   Approach 1: Baseline DeepSORT
```bash
# Run detection
python player_reid_single_feed/src/detect.py --threshold 0.5

# Extract appearance features
python player_reid_single_feed/src/extract_appearance_features.py

# Track players (default DeepSORT config)
python player_reid_single_feed/src/track_deepsort.py --config configs/baseline.yaml

# Merge and interpolate
python player_reid_single_feed/src/merge_tracks.py
python player_reid_single_feed/src/interpolate_tracks.py

# Visualize results
python player_reid_single_feed/src/visualize_tracks.py --output approach1.mp4
```
  Approach 2: Lowered Detection Threshold & Tuned DeepSORT
```bash
python player_reid_single_feed/src/detect.py --threshold 0.3
python player_reid_single_feed/src/track_deepsort.py --config configs/tuned.yaml
```

Approach 3: Best Balance (Further Tuning)
```bash
python player_reid_single_feed/src/detect.py --threshold 0.2
python player_reid_single_feed/src/track_deepsort.py --config configs/flexible.yaml
```

Approach 4: Appearance-based Association + Occlusion Handling
```bash
python player_reid_single_feed/src/detect.py --threshold 0.2
python player_reid_single_feed/src/track_deepsort.py --config configs/appearance.yaml
python player_reid_single_feed/src/merge_tracks.py --use-appearance
python player_reid_single_feed/src/interpolate_tracks.py
```

5. **Visualize results**

```bash
python player_reid_single_feed/src/visualize_tracks.py
```

## Future Improvements

- Upgrade to YOLOv8 or Faster R-CNN for detection.
- Fine-tune ReID model on custom dataset.
- Implement advanced association strategies.
- Improve occlusion handling and track merging.
- Quantitatively evaluate with MOTA, IDF1, etc.


A brief report containing approaches , methodology and their outcomes has been attached - report.md file


