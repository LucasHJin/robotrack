from ultralytics import YOLO

# USE MODAL

# n, s, m, l, x
model = YOLO('yolov8l.pt') # load pretrained model weights

# note -> add augmentations + preprocessing
model.train(data='custom_dataset.yaml',
        epochs=50,
        imgsz=640,
        batch=16,
        device=0)