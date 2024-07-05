### Libraries

import pandas as pd
import numpy as np

from io import BytesIO
from io import StringIO
import json

import pytube
from pydub import AudioSegment
from moviepy.editor import AudioFileClip

import librosa
import librosa.display

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from glob import glob
import os 

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

### Setting up the page

st.title('Working with audio file using python')
st.divider()
st.write('This project aims to search a video on youtube, get the audio and perform some analysis')
st.divider()

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
    data, samplerate = sf.read(buffer)
    st.write("sucessfully read")
    librosa_audio_data = librosa.resample(data.T, samplerate, 22050)
    st.write("data is in librosa")
    #filename = yt.streams.filter(only_audio=True).first().download(filename='test.mp4')
    #st.write(os.listdir())
    # audio = AudioFileClip(filename)
    # audio.write_audio("output.wav", codec='pcm_s16le')
    # st.write(os.listdir())

    # sound = AudioSegment.from_file("/mount/src/working_with_audio_signal/test.mp4",format="mp4")
    # sound.export("/mount/src/working_with_audio_signal/test.wav", format="wav")
    # audio_files = glob('/mount/src/test.wav')
    # y, sr = librosa.load(audio_files[0])
    # st.audio(audio_files)

