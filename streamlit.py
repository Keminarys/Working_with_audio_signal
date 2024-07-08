### Libraries

import pandas as pd
import numpy as np

from io import BytesIO
from io import StringIO
import json

import pytube
from pydub import AudioSegment
from moviepy.editor import AudioFileClip
import soundfile as sf
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

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

### Setting up the page

st.title('Working with audio file using python')
st.divider()
st.write('This project aims to search a video on youtube, get the audio and perform some analysis')
st.divider()

### Function
def convert_mp4_to_wav_ffmpeg_bytes2bytes(input_data: bytes) -> bytes:
    """
    It converts mp3 to wav using ffmpeg
    :param input_data: bytes object of a mp3 file
    :return: A bytes object of a wav file.
    """
    args = (ffmpeg
            .input('pipe:', format='mp4')
            .output('pipe:', format='wav')
            .global_args('-loglevel', 'error')
            .get_args()
            )
    # print(args)
    proc = subprocess.Popen(
        ['ffmpeg'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return proc.communicate(input=input_data)[0]

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
    yt = pytube.YouTube(url_total_vid)
    audio_stream = yt.streams.filter(only_audio=True).first()
    buffer=BytesIO()
    audio_stream.stream_to_buffer(buffer)
    buffer.seek(0)

    wav_file = convert_mp4_to_wav_ffmpeg_bytes2bytes(buffer)
    st.write("All good !")
    
    # y, sr = librosa.load(audio_files[0])
