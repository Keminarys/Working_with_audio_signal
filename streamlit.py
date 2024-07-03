
import pandas as pd
import numpy as np

import pytube
from pydub import AudioSegment
from io import BytesIO
import librosa
import librosa.display

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from glob import glob

st.title('Working with audio file using python')
st.divider()
st.write('This project aims to search a video on youtube, get the audio and perform some analysis')
st.divider()


# gauth = GoogleAuth()
# drive = GoogleDrive(gauth)

# # Télécharger un fichier audio
# audio_file = drive.CreateFile({'title': 'temp.mp4'})
# audio_file.SetContentFile('temp.mp4')
# audio_file.Upload()
# print('Le fichier audio a été téléchargé avec succès.')

# # Lire le fichier audio
# file_id = audio_file['id']
# audio_file = drive.CreateFile({'id': file_id})
# audio_file.GetContentFile('MonFichierAudio.mp3')
# print('Le fichier audio a été lu avec succès.')
