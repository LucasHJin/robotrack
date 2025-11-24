import cv2
import subprocess # needed to run CLI commands like yt-dlp and ffmpeg
import numpy as np
import os

youtube_url = "https://www.youtube.com/watch?v=iO5byiwVXVw"
output_dir = "data"
frame_skip = 30
os.makedirs(output_dir, exist_ok=True)


def video_stats():
    # get width and height of chosen youtube video
    probe_cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "--print", "%(width)s",
        "--print", "%(height)s",
        youtube_url
    ]
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    width, height = map(int, result.stdout.strip().split('\n'))
    return width, height

def stream_video():
    width, height = video_stats()
    
    # get video as live data stream
    yt_command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "-o", "-",
        youtube_url
    ]

    # reads in data stream and converts to video frames
    ffmpeg_command = [
        "ffmpeg",
        "-i", "pipe:0",
        "-vf", f"scale={width}:{height}",
        "-f", "image2pipe",
        "-pix_fmt", "bgr24",
        "-vcodec", "rawvideo",
        "-"
    ]

    yt_process = subprocess.Popen(yt_command, stdout=subprocess.PIPE)
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=yt_process.stdout, stdout=subprocess.PIPE) # connect sp with pipes

    # get every 30th frame
    frame_count = 0
    saved_count = 0
    while True:
        raw_frame = ffmpeg_process.stdout.read(width * height * 3) # type: ignore
        if len(raw_frame) != width * height * 3: # run out of frames
            break
        
        frame = np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3)) # convert raw bytes into image array
        
        if frame_count % frame_skip == 0:
            cv2.imwrite(os.path.join(output_dir, f"frame_{saved_count:05d}.jpg"), frame)
            saved_count += 1
        
        frame_count += 1

    ffmpeg_process.stdout.close() # type: ignore
    yt_process.stdout.close() # type: ignore
    ffmpeg_process.wait()
    yt_process.wait()
    
print(video_stats())