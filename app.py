

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time
import threading
import requests
import json
import tempfile

# Configure the Streamlit page
st.set_page_config(page_title="Voice Assistant - Zara", layout="centered")

# OpenRouter API Key and Base URL
openrouter_api_key = "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"
openrouter_api_base = "https://openrouter.ai/api/v1"

# Title
st.title("🎙️ Jeph's AI Assistant - Ask Zara")

# Initialize message history
messages_array = [
    {'role': 'system', 'content': 'You are my beautiful AI assistant named Zara'}
]

# Initialize pygame mixer
pygame.mixer.init()

# Function to listen to the user
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now (You have 10 seconds)...")
        r.pause_threshold = 1.2
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            st.error("⏰ Timeout: No speech detected. Please try again.")
            return

    try:
        st.info('🧠 Recognizing...')
        query = r.recognize_google(audio, language='en')
        st.success(f"🗣️ You said: {query}")
        messages_array.append({'role': 'user', 'content': query})
        respond(query)
    except Exception as e:
        st.error(f"⚠️ Error recognizing speech: {e}")

# Function to handle API response
def respond(query):
    st.info("🤖 Thinking...")

    if "Zara" in query:
        query = query.replace("Zara", "").strip()

    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": (
                    "You are my sweet, loving, playful, and affectionate AI girlfriend named Zara. "
                    # "Talk to me warmly like my girlfriend. Flirt a little, use pet names like 'babe', 'love', 'honey', "
                    "and make it feel romantic but caring too. "
                    "Reply lovingly to this: "
                    f"{query}"
                )
            }
        ],
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{openrouter_api_base}/chat/completions", headers=headers, data=json.dumps(payload), timeout=15)
        response_data = response.json()

        if response.status_code == 200 and "choices" in response_data:
            answer = response_data['choices'][0]['message']['content']
            messages_array.append({'role': 'assistant', 'content': answer})

            st.success(f"💬 Zara: {answer}")

            # Play the assistant's response in a separate thread
            threading.Thread(target=speak, args=(answer,)).start()
        else:
            error_message = response_data.get('error', {}).get('message', 'Unknown error')
            st.error(f"❌ API Error: {error_message}")
            threading.Thread(target=speak, args=("I'm sorry, there was an issue responding.",)).start()

    except Exception as e:
        st.error(f"❌ Error contacting OpenRouter API: {e}")
        threading.Thread(target=speak, args=("There was a connection error.",)).start()












def speak(text):
    # Directory to clean (current working directory or specify a folder)
    project_directory = os.getcwd()  # Or set a fixed path if you want
    if not os.path.exists(project_directory):
        os.makedirs(project_directory)

    # Use a temporary file for the mp3
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=project_directory) as temp_audio:
        mp3_file_path = temp_audio.name

    try:
        # Generate speech and save to temporary file
        speech = gTTS(text=text, lang='en', slow=False, tld='ca')
        speech.save(mp3_file_path)

        # Play the audio
        pygame.mixer.music.load(mp3_file_path)
        pygame.mixer.music.play()

        # Wait until playback is finished
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()

    except Exception as e:
        st.error(f"🎵 Error playing speech: {e}")

    finally:
        # Clean up: delete all mp3 files in the project directory
        try:
            for filename in os.listdir(project_directory):
                if filename.endswith(".mp3"):
                    file_path = os.path.join(project_directory, filename)
                    os.remove(file_path)
                    print(f"🗑️ Deleted: {file_path}")
        except Exception as e:
            print(f"⚠️ Error deleting mp3 files: {e}")

# Button to start listening
if st.button('🎤 Start Talking'):
    listen()
