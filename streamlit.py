### Libraries

import pandas as pd
import numpy as np

from io import BytesIO
from io import StringIO
import json

import pytube
from pydub import AudioSegment

import librosa
import librosa.display

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from glob import glob

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

### Setting up the page

st.title('Working with audio file using python')
st.divider()
st.write('This project aims to search a video on youtube, get the audio and perform some analysis')
st.divider()

### Function

def download_youtube_video(url):
    yt = pytube.YouTube(url)
    stream = yt.streams.first()
    
    # Download the video to a BytesIO object in memory
    audio_file = BytesIO()
    audio_file.write(stream.download(path=None))
    audio_file.seek(0)
    
    return audio_file

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
    audio_file = download_youtube_video(url_total_vid)
    st.write(type(audio_file))
    # sound = AudioSegment.from_file("/mount/src/working_with_audio_signal/test.mp4",format="mp4")
    # sound.export("/mount/src/working_with_audio_signal/test.wav", format="wav")
    # audio_files = glob('/mount/src/test.wav')
    # y, sr = librosa.load(audio_files[0])
    # st.audio(audio_files)
