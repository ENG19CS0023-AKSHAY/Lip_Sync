import cv2
import torch
import torchaudio
from moviepy.editor import *

def torch_resample_waveform(waveform, new_sample_rate):
    transform = torchaudio.transforms.Resample(orig_freq=waveform.shape[1], new_freq=new_sample_rate)
    return transform(waveform)

# Read the video and audio files
video_path = "video.mp4"
audio_path = "output10.wav"  
# Read the video frames using OpenCV
video_capture = cv2.VideoCapture(video_path)
video_frames = []
while True:
    success, frame = video_capture.read()
    if not success:
        break
    video_frames.append(frame)
video_capture.release()

# Read the audio file using torch
waveform, sample_rate = torchaudio.load(audio_path)

# Convert the audio to stereo (if needed)
if len(waveform.shape) == 1:
    waveform = torch.stack([waveform, waveform])

# Resample the audio waveform to match the video frame rate
audio_duration = len(waveform) / sample_rate
frame_rate = len(video_frames) / audio_duration

# Check if frame_rate is zero
if frame_rate == 0:
    raise Exception("The frame rate of the video is zero. Please check the video file or try a different video.")

resampled_waveform = torch_resample_waveform(waveform, int(len(waveform) * frame_rate / sample_rate))

# Combine audio and video
audio_clip = AudioFileClip(audio_path)
video_clip = ImageSequenceClip(video_frames, fps=frame_rate)
final_clip = video_clip.set_audio(audio_clip)
final_clip.write_videofile("output_video.mp4", codec="libx264")
