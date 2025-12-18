from ultralytics import YOLO # type: ignore

model = YOLO('./model/best.pt')

for result in model.predict(
    source='test_data/test_match2.mp4',
    conf=0.5,
    save=True,
    stream=True,
):
    pass