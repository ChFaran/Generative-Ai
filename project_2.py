# Install necessary packages
!pip install streamlit magenta tensorflow pyngrok

# Create the Streamlit app script
app_code = """
import streamlit as st
import requests
import tempfile
from magenta.models.music_vae import TrainedModel, configs
from magenta.protobuf import music_pb2
import magenta.music as mm
import numpy as np
import tensorflow as tf

# Deezer API base URL
DEEZER_API_URL = "https://api.deezer.com/search"

# Function to search for songs using Deezer API
def search_song(query):
    params = {'q': query}
    response = requests.get(DEEZER_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        st.error("Failed to fetch data from Deezer API.")
        return []

# Load Magenta's pre-trained Melody RNN model
def load_model():
    model_name = 'cat-mel_2bar_big'
    model_config = configs.CONFIG_MAP[model_name]
    checkpoint_dir = tempfile.mkdtemp()
    model = TrainedModel(
        model_config,
        batch_size=1,
        checkpoint_dir_or_path=model_config.checkpoint_file
    )
    return model

# Generate a melody using Magenta's Melody RNN
def generate_melody(model):
    primer_sequence = music_pb2.NoteSequence()
    generated_sequence = model.sample(n=1, primer_sequence=primer_sequence)[0]
    midi = mm.sequence_proto_to_midi_file(generated_sequence)
    return midi

# Streamlit UI
st.title("Music Finder & Generator")

# Tabs for Deezer Search and Melody Generation
tab1, tab2 = st.tabs(["Deezer Song Search", "Magenta Melody Generator"])

with tab1:
    st.header("Search for Songs on Deezer")
    query_deezer = st.text_input("Search for a song or artist on Deezer:")
    
    if query_deezer:
        songs = search_song(query_deezer)
        if songs:
            st.write(f"Found {len(songs)} results for '{query_deezer}':")
            for song in songs:
                song_title = song['title']
                artist_name = song['artist']['name']
                preview_url = song['preview']

                st.write(f"*{song_title}* by {artist_name}")
                st.audio(preview_url)
        else:
            st.write("No songs found. Try a different search term.")

with tab2:
    st.header("Generate a Melody with Magenta")
    if st.button("Generate Melody"):
        try:
            # Load the model
            model = load_model()
            # Generate a melody
            midi_file = generate_melody(model)
            # Save to a temporary file and display
            with open("generated_melody.mid", "wb") as f:
                f.write(midi_file)
            st.write("Generated Melody:")
            st.audio("generated_melody.mid")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Run the app
# To run this app, save it as app.py and run streamlit run app.py in your terminal.
"""

# Write the app code to app.py
with open("app.py", "w") as f:
    f.write(app_code)

# Install and import pyngrok for creating a tunnel
!pip install pyngrok
from pyngrok import ngrok

# Run the Streamlit server in the background
!streamlit run app.py &

# Create an ngrok tunnel to the Streamlit app
public_url = ngrok.connect(port='8501')
public_url
