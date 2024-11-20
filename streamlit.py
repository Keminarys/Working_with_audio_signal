### Libraries

import pandas as pd
import numpy as np

import random
from datetime import datetime, timedelta

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

st.title('Audio Signal Processing 🎶')
st.divider()
st.write('With this little app, I wanted to dive into signal audio processing.')
st.write('Depends on your needs, you can either create a sound from scratch using trigonometry or search for a sound on youtube.')
st.divider()

tab1, tab2, tabTest = st.tabs(["Create your own soundwave", "Look for sound on YouTube", "POC Maggio"])

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
    yt = pytube.YouTube(url)
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
with tab1 : 
    st.write("Fun way to understand how signal audio works")
    st.write("Using trigonometry, you can create audio signal")
    alpha = st.slider("Pick your α (Decay value)", 0.00, 1.00, 0.01)
    M = st.number_input("Input a value for M (nb of sample)")
    
with tab2 :
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
          audio_files = glob(str(save_location))
          y, sr = librosa.load(audio_files[0])
          st.write(f'y: {y[:10]}')
          st.write(f'shape y: {y.shape}')
          st.write(f'sr: {sr}')

with tabTest : 

    st.write("Merci de choisir le nombre de camion et le nombre de point à générer")
    num_trucks = st.number_input("Nombre de camion", step=1)
    num_trucks = int(num_trucks)
    base_location = (43.4368, 5.2156)  # Coordinates for Aéroport Marseille Provence
    radius = 200 / 111  # Approx. radius in degrees (1 degree ≈ 111 km)
    start_date = datetime(2024, 11, 15)
    end_date = datetime(2024, 11, 20)
    num_points = st.number_input("Nombre de point par camion", step=1) # Number of data points per truck
    num_points = int(num_points)
    nb_min = st.number_input("Intervalle en minute", step=1)
    nb_min = int(nb_min)
    interval = timedelta(minutes=nb_min)
    hours_per_day = 12
    
    if num_trucks != 0 and num_points != 0 :
        # Generate random data
        data = []
        for truck_id in range(1, num_trucks + 1):
            current_time = start_date
            while current_time <= end_date:
                for hour in range(7, 19):  # From 7 AM to 7 PM
                    time_point = current_time.replace(hour=hour, minute=0, second=0, microsecond=0)
                    for _ in range(0, 60, 15):  # Every 15 minutes
                        lat = base_location[0] + random.uniform(-radius, radius)
                        lon = base_location[1] + random.uniform(-radius, radius)
                        data.append([truck_id, time_point, lat, lon])
                        time_point += interval
                current_time += timedelta(days=1)
        st.write(f'Génération de données pour {num_trucks} camions')
        if st.button("Générer des data au hasard"):
            df = pd.DataFrame(data, columns=['Truck ID', 'Timestamp', 'Latitude', 'Longitude'])
            st.dataframe(df)
        st.divider()
        st.write("Visualiser le tracking")
        if st.button("Voir le tracking") :
            start_time = st.slider("Date et Heure", value=df.Timestamp.min())
            df_filtered = df.loc[df.Timestamp == start_time)
            st.map(df_filtered, latitude="Latitude", longitude="Longitude", color="Truck ID")

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
