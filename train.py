import modal

"""
first model
    prediction: 95.3
    recall: 91.3
    mAP50: 96.4
    mAP50-95: 0.703
"""

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


@app.function(volumes={"/data": volume}, gpu="L40S", timeout=36000, retries=1)
def train():
    from ultralytics import YOLO # type: ignore

    model = YOLO("yolov8x.pt")

    results = model.train(
        data="/data/dataset/data.yaml",
        epochs=120,
        imgsz=1280,
        batch=16,
        project="/data/runs",
        name="frc-v2",
        patience=15,
        
        #augmentation
        degrees=5,
        shear=2,
        mixup=0.1,
        hsv_v=0.5,
        hsv_h=0.03,
        hsv_s=0.75,
        copy_paste=0.1
    )
    
    volume.commit()
    
    return results

@app.local_entrypoint()
def main():
    train.remote()
    
