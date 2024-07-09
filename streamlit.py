### Libraries

import pandas as pd
import numpy as np

from io import BytesIO
import subprocess

import pytube
import ffmpeg

import librosa
import librosa.display

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from glob import glob
import os 
from pathlib import Path

import torch
from miniaudio import SampleFormat, decode
### Setting up the page

st.title('Working with audio file using python')
st.divider()
st.write('This project aims to search a video on youtube, get the audio and perform some analysis')
st.divider()

### Function
def convert_mp3_to_wav_ffmpeg_bytes2bytes(input_data: bytes) -> bytes:
    args = (ffmpeg
            .input('pipe:', format='mp3')
            .output('pipe:', format='wav')
            .global_args('-loglevel', 'error')
            .get_args()
            )
    st.write(args)
    proc = subprocess.Popen(
        ['ffmpeg'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return proc.communicate(input=input_data)[0]


def save_audio(url):
    yt = YouTube(url)
    try:
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download()
    except:
        return None, None, None
    base, ext = os.path.splitext(out_file)
    file_name = base + '.mp3'
    os.rename(out_file, file_name)
    print(yt.title + " has been successfully downloaded.")
    print(file_name)
    return yt.title, file_name, yt.thumbnail_url
### Main app

textinput = st.text_input("Please enter your keywords to find the desired video here", "")
if len(textinput) > 0 :
  s = pytube.Search(textinput)
  url_fixed = "https://www.youtube.com/watch?v="
  url_moving = str(s.results[0])[-12:]
  url_total_vid = url_fixed+url_moving
  
  st.write("Is that the video you wanted ?")
  st.video(url_total_vid)
  if st.button("Yes"):
      video_title, save_location, video_thumbnail = save_audio(url_total_vid)
      st.audio(save_location)
      st.write(video_title)
    # yt = pytube.YouTube(url_total_vid)
    # audio_stream = yt.streams.filter(only_audio=True).first()
    # buffer=BytesIO()
    # st.write(buffer.getbuffer().nbytes)
    # audio_stream.stream_to_buffer(buffer)
    # buffer.seek(0)
    # st.write(buffer.getbuffer().nbytes)
    # decoded_audio = decode(buffer, output_format=SampleFormat.SIGNED32)
    # decoded_audio = torch.FloatTensor(decoded_audio.samples)
    # decoded_audio /= (1 << 31)
    # st.write(decoded_audio.max())
    # st.write(decoded_audio.min())
    # st.write(decoded_audio.shape)
    # st.write(decoded_audio.dtype)
    #st.pyplot(plt.plot(decoded_audio.numpy(), linewidth=1))

    # wav_file = convert_mp4_to_wav_ffmpeg_bytes2bytes(buffer)
    # st.write("All good !")
    
    # y, sr = librosa.load(audio_files[0])
