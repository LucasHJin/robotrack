from frame_extraction import stream_video
from frame_validation import validate_frame

VIDEO_LIST = [
    "https://www.youtube.com/watch?v=EujMnWlD6lg",
    "https://www.youtube.com/watch?v=2LXaPNCmuH0",
    "https://www.youtube.com/watch?v=wfZUS3Fex3Q",
    "https://www.youtube.com/watch?v=o8mD86_97C4",
    "https://www.youtube.com/watch?v=TIoRXU5pjT0",
    "https://www.youtube.com/watch?v=EtyToHXGbHM",
    "https://www.youtube.com/watch?v=uLkk8m1qH3E",
    "https://www.youtube.com/watch?v=040jq4AvU2U",
    "https://www.youtube.com/watch?v=H-dxnTfXKyc",
    "https://www.youtube.com/watch?v=fjdm790hFT8"
]

for count, video in enumerate(VIDEO_LIST):
    stream_video(60, video, "data/raw", count)
    
validate_frame("data/raw", "data/clean")