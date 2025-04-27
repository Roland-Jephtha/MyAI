import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import json
import tempfile
import requests
import time
import base64
import glob
from datetime import datetime, timedelta


# Configure the Streamlit page
st.set_page_config(page_title="Voice Assistant - Zara", layout="centered")

# OpenRouter API Key and Base URL
openrouter_api_key = "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"
openrouter_api_base = "https://openrouter.ai/api/v1"

# Title
st.title("🎙️ Jeph's AI Assistant -- Zara")

# Initialize message history
messages_array = [
    {'role': 'system', 'content': 'You are my beautiful AI assistant named Zara'}
]





def clean_old_audio_files(directory=".", extension="mp3", keep_minutes=1):
    """Delete all .mp3 files older than `keep_minutes` in the given directory."""
    now = datetime.now()
    cutoff_time = now - timedelta(minutes=keep_minutes)

    # Find all mp3 files in the directory
    files = glob.glob(os.path.join(directory, f"*.{extension}"))

    for file_path in files:
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        if file_mtime < cutoff_time:
            try:
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")


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
        response = requests.post(
            f"{openrouter_api_base}/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=15
        )
        response_data = response.json()

        if response.status_code == 200 and "choices" in response_data:
            answer = response_data['choices'][0]['message']['content']
            messages_array.append({'role': 'assistant', 'content': answer})
            st.success(f"💬 Zara: {answer}")

            # Speak and play response
            speak(answer)

        else:
            error_message = response_data.get('error', {}).get('message', 'Unknown error')
            st.error(f"❌ API Error: {error_message}")
            speak("I'm sorry, there was an issue responding.")

    except Exception as e:
        st.error(f"❌ Error contacting OpenRouter API: {e}")
        speak("There was a connection error.")

def speak(text):
    try:
        clean_old_audio_files()  # Clean before saving new audio

        tts = gTTS(text=text, lang='en', slow=False, tld='ca')

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=".") as tmpfile:
            tts.save(tmpfile.name)
            tmpfile_path = tmpfile.name

        # Inject an invisible HTML audio player
        audio_html = f"""
        <audio autoplay="true" style="display:none;">
            <source src="data:audio/mp3;base64,{base64.b64encode(open(tmpfile_path, 'rb').read()).decode()}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

        # Clean up the temp file after a short delay
        time.sleep(5)
        if os.path.exists(tmpfile_path):
            os.remove(tmpfile_path)

    except Exception as e:
        st.error(f"🎵 Error playing speech: {e}")


# Button to start listening
if st.button('🎤 Start Talking'):
    listen()





