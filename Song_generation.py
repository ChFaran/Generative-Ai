import streamlit as st
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import io
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-to-audio", model="facebook/musicgen-small")
# Load model directly
from transformers import AutoTokenizer, AutoModelForTextToWaveform

tokenizer = AutoTokenizer.from_pretrained("facebook/musicgen-small")
model = AutoModelForTextToWaveform.from_pretrained("facebook/musicgen-small")

# Define Deezer API search endpoint
DEEZER_API_URL = "https://api.deezer.com/search"

# Define Hugging Face model details
#HUGGINGFACE_TOKEN = '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'  # Enter your Hugging Face token here
#MODEL_NAME = "facebook/musicgen-small"  # Replace with the actual model name if different

# Initialize Hugging Face model and tokenizer
#tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=HUGGINGFACE_TOKEN)
#model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, use_auth_token=HUGGINGFACE_TOKEN)

# Function to search for songs
def search_song(query):
    params = {
        'q': query
    }
    response = requests.get(DEEZER_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        return []

# Function to generate music
def generate_music(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Streamlit UI
st.title("Song Finder & Music Generator")

# Search bar
query = st.text_input("Search for a song or artist:")

if query:
    # Search for songs
    songs = search_song(query)
    if songs:
        st.write(f"Found {len(songs)} results for '{query}':")
        for song in songs:
            song_title = song['title']
            artist_name = song['artist']['name']
            preview_url = song['preview']

            st.write(f"**{song_title}** by {artist_name}")
            st.audio(preview_url)
    else:
        st.write("No songs found. Try a different search term.")

    # Generate music based on search query
    if st.button("Generate Music"):
        st.write("Generating music...")
        generated_music = generate_music(query)
        st.write(f"Generated Music:\n{generated_music}")

        # Optionally, save the generated music to a file if it's in a text format
        if generated_music:
            with open('generated_music.txt', 'w') as file:
                file.write(generated_music)
            st.write("Music saved to 'generated_music.txt'.")
