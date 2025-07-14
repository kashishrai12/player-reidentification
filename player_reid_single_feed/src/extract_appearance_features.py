import torchreid
import cv2
import json
import torch
import torchvision.transforms as T

# Load model
model = torchreid.models.build_model(
    name='osnet_x1_0', num_classes=1000, pretrained=True
)
model.eval()

# Add preprocessing for Torchreid
preprocess = T.Compose([
    T.ToPILImage(),
    T.Resize((256, 128)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Extract features for each detection
with open("../data/detections_filtered.json") as f:
    detections = json.load(f)

cap = cv2.VideoCapture("../data/15sec_input_720p.mp4")
features = []
for d in detections:
    cap.set(cv2.CAP_PROP_POS_FRAMES, d['frame'])
    ret, frame = cap.read()
    x1, y1, x2, y2 = map(int, d['bbox'])
    crop = frame[y1:y2, x1:x2]
    if crop.size == 0:
        features.append([0]*2048)  # or whatever your feature size is
        continue
    inp = preprocess(crop).unsqueeze(0)  # shape: (1, 3, 256, 128)
    with torch.no_grad():
        feat = model(inp).cpu().numpy().flatten().tolist()
    d['appearance_feat'] = feat
    features.append(feat)

with open("../data/detections_with_features.json", "w") as f:
    json.dump(detections, f, indent=2)