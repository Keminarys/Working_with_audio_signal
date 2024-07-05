
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

st.title('Working with audio file using python')
st.divider()
st.write('This project aims to search a video on youtube, get the audio and perform some analysis')
st.divider()

### Function : 
def upload_to_drive(file_path):
    gauth = GoogleAuth(settings_file=json.load(StringIO(st.secrets["client_secrets"])))
    drive = GoogleDrive(gauth)
    
    file_drive = drive.CreateFile({'title': file_path})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()


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
    yt.streams.filter(only_audio=True).first().download(filename='test.mp4')
    sound = AudioSegment.from_file("/mount/src/working_with_audio_signal/test.mp4",format="mp4")
    sound.export("/mount/src/working_with_audio_signal/test.wav", format="wav")
    # audio_files = glob('/mount/src/test.wav')
    # y, sr = librosa.load(audio_files[0])
    # st.audio(audio_files)
