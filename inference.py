from ultralytics import YOLO # type: ignore

model = YOLO('./model/best.pt')

results = model('path/to/video.mp4', save=True)

results = model.track( 
    source='test_match.mp4',
    save=True,
    tracker='botsort.yaml', # track across frames
    conf=0.5,
)