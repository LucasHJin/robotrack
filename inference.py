from ultralytics import YOLO # type: ignore

model = YOLO('./model/best.pt')


# track doesn't work (loses track)
results = model.track( 
    source='test_match.mp4',
    save=True,
    tracker='botsort.yaml', # track across frames
    conf=0.5,
)