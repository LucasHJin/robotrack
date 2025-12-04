import modal

image = modal.Image.debian_slim().apt_install(
        "libgl1-mesa-glx", # need these libraries for opencv
        "libglib2.0-0",
    ).pip_install(
    "ultralytics",
    "torch",
    "torchvision",
    "opencv-python-headless",
    "pillow",
)

app = modal.App("frc-training", image=image)

volume = modal.Volume.from_name("frc", create_if_missing=True)


@app.function(volumes={"/data": volume}, gpu="L40S", timeout=43200, retries=1)
def train():
    from ultralytics import YOLO

    model = YOLO("yolov8l.pt")

    results = model.train(
        data="/data/dataset/data.yaml",
        epochs=80,
        imgsz=640,
        batch=32,
        project="/data/runs",
        name="frc-v1",
        patience=10,
        
        #augmentation
        degrees=5,
        shear=2,
        mixup=0.05,
        hsv_v=0.6,
    )
    
    volume.commit()
    
    return results

@app.local_entrypoint()
def main():
    train.remote()
    
