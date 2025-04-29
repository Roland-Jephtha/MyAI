

# # import streamlit as st
# # from gtts import gTTS
# # import os
# # import json
# # import tempfile
# # import requests
# # import time
# # import base64
# # import glob
# # from datetime import datetime, timedelta
# # from dotenv import load_dotenv
# # import streamlit.components.v1 as components


# # # Load environment variables
# # load_dotenv()


# # # Configure the Streamlit page
# # st.set_page_config(page_title="Voice Assistant - Zara", layout="centered")

# # # OpenRouter API Key and Base URL
# # openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
# # openrouter_api_base = "https://openrouter.ai/api/v1"

# # # Title
# # st.title("🎙️ Jeph's AI Assistant -- Zara")

# # # Initialize message history
# # messages_array = [
# #     {'role': 'system', 'content': 'You are my beautiful AI assistant named Zara'}
# # ]

# # # Function to clean old audio files
# # def clean_old_audio_files(directory=".", extension="mp3", keep_minutes=1):
# #     """Delete all .mp3 files older than `keep_minutes` in the given directory."""
# #     now = datetime.now()
# #     cutoff_time = now - timedelta(minutes=keep_minutes)

# #     # Find all mp3 files in the directory
# #     files = glob.glob(os.path.join(directory, f"*.{extension}"))

# #     for file_path in files:
# #         file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
# #         if file_mtime < cutoff_time:
# #             try:
# #                 os.remove(file_path)
# #                 print(f"Deleted old file: {file_path}")
# #             except Exception as e:
# #                 print(f"Error deleting file {file_path}: {e}")

# # # Function to listen to the user using JavaScript
# # def listen():
# #     st.info("🎤 Listening... Speak now (click Allow Microphone)...")

# #     # JavaScript for speech recognition
# #     components.html(
# #         """
# #         <script>
# #         const streamlitAudioRecognition = () => {
# #             const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
# #             const recognition = new SpeechRecognition();
# #             recognition.lang = 'en-US';
# #             recognition.interimResults = false;
# #             recognition.maxAlternatives = 1;

# #             recognition.start();

# #             recognition.onresult = (event) => {
# #                 const transcript = event.results[0][0].transcript;
# #                 console.log('You said: ', transcript);
# #                 const streamlitEvent = new CustomEvent("streamlit:message", {
# #                     detail: { type: "speech", data: transcript }
# #                 });
# #                 window.parent.document.dispatchEvent(streamlitEvent);
# #             };

# #             recognition.onerror = (event) => {
# #                 const streamlitEvent = new CustomEvent("streamlit:message", {
# #                     detail: { type: "error", data: event.error }
# #                 });
# #                 window.parent.document.dispatchEvent(streamlitEvent);
# #             };
# #         };

# #         streamlitAudioRecognition();
# #         </script>
# #         """,
# #         height=0,
# #         width=0,
# #     )

# # # Function to handle API response
# # def respond(query):
# #     st.info("🤖 Thinking...")

# #     if "Zara" in query:
# #         query = query.replace("Zara", "").strip()

# #     payload = {
# #         "model": "openai/gpt-4o",
# #         "messages": [
# #             {
# #                 "role": "user",
# #                 "content": (
# #                     "You are my sweet, smart, Knowledgeable, loving, playful, and affectionate AI female friend named Zara. "
# #                     "Reply lovingly to this: "
# #                     f"{query}"
# #                 )
# #             }
# #         ],
# #         "max_tokens": 500
# #     }

# #     headers = {
# #         "Authorization": f"Bearer {openrouter_api_key}",
# #         "Content-Type": "application/json"
# #     }

# #     try:
# #         response = requests.post(
# #             f"{openrouter_api_base}/chat/completions",
# #             headers=headers,
# #             data=json.dumps(payload),
# #             timeout=15
# #         )
# #         response_data = response.json()

# #         if response.status_code == 200 and "choices" in response_data:
# #             answer = response_data['choices'][0]['message']['content']
# #             messages_array.append({'role': 'assistant', 'content': answer})
# #             st.success(f"💬 Zara: {answer}")

# #             # Speak and play response



# #             speak(answer)
# #             return answer



# #         else:
# #             error_message = response_data.get('error', {}).get('message', 'Unknown error')
# #             st.error(f"❌ API Error: {error_message}")
# #             speak("I'm sorry, there was an issue responding.")

# #     except Exception as e:
# #         st.error(f"❌ Error contacting OpenRouter API: {e}")
# #         speak("There was a connection error.")




# # def speak(text):
# #     try:
# #         clean_old_audio_files()  # Clean before saving new audio

# #         tts = gTTS(text=text, lang='en', slow=False, tld='ca')

# #         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=".") as tmpfile:
# #             tts.save(tmpfile.name)
# #             tmpfile_path = tmpfile.name

# #         # Inject an invisible HTML audio player
# #         audio_html = f"""
# #         <audio autoplay="true" style="display:none;">
# #             <source src="data:audio/mp3;base64,{base64.b64encode(open(tmpfile_path, 'rb').read()).decode()}" type="audio/mp3">
# #         </audio>
# #         """
# #         st.markdown(audio_html, unsafe_allow_html=True)

# #         # Clean up the temp file after a short delay
# #         time.sleep(5)
# #         if os.path.exists(tmpfile_path):
# #             os.remove(tmpfile_path)

# #     except Exception as e:
# #         st.error(f"🎵 Error playing speech: {e}")

# # # Listen for message back
# # if st.button('🎤 Start Talking'):
# #     listen()

# # # Add an event listener to capture the transcript returned from JS and pass it to Streamlit
# # components.html(
# #     """
# #     <script>
# #     window.parent.document.addEventListener("streamlit:message", function(event) {
# #         if (event.detail.type === "speech") {
# #             // Send the result to Streamlit
# #             window.location.href = "?speech=" + encodeURIComponent(event.detail.data);
# #         }
# #     });
# #     </script>
# #     """,
# #     height=0,
# #     width=0,
# # )

# # # Capture the speech input passed back to Streamlit using the updated `st.query_params`
# # speech = st.query_params.get("speech")

# # if speech:
# #     query = speech[0]
# #     st.success(f"🗣️ You said: {query}")
# #     messages_array.append({'role': 'user', 'content': query})
# #     respond(query)
# # else:
# #     # st.warning("⏳ Waiting for speech input...")
# #     pass














# import streamlit as st
# from gtts import gTTS
# import os
# import json
# import tempfile
# import requests
# import time
# import base64
# import glob
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import streamlit.components.v1 as components

# # Load environment variables
# load_dotenv()

# # Configure the Streamlit page
# st.set_page_config(page_title="Voice Assistant - Zara", layout="centered")

# # OpenRouter API Key and Base URL
# openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
# openrouter_api_base = "https://openrouter.ai/api/v1"

# # Title
# st.title("🎙️ Jeph's AI Assistant -- Zara")

# # Initialize message history
# messages_array = [{'role': 'system', 'content': 'You are my beautiful AI assistant named Zara'}]

# # Function to clean old audio files
# def clean_old_audio_files(directory=".", extension="mp3", keep_minutes=1):
#     """Delete all .mp3 files older than `keep_minutes` in the given directory."""
#     now = datetime.now()
#     cutoff_time = now - timedelta(minutes=keep_minutes)
#     files = glob.glob(os.path.join(directory, f"*.{extension}"))
#     for file_path in files:
#         file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
#         if file_mtime < cutoff_time:
#             try:
#                 os.remove(file_path)
#                 print(f"Deleted old file: {file_path}")
#             except Exception as e:
#                 print(f"Error deleting file {file_path}: {e}")

# # Function to listen to the user using JavaScript
# def listen():
#     st.info("🎤 Listening... Speak now (click Allow Microphone)...")

#     # JavaScript for speech recognition
#     components.html(
#         """
#         <script>
#         const streamlitAudioRecognition = () => {
#             const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
#             const recognition = new SpeechRecognition();
#             recognition.lang = 'en-US';
#             recognition.interimResults = false;
#             recognition.maxAlternatives = 1;

#             recognition.start();

#             recognition.onresult = (event) => {
#                 const transcript = event.results[0][0].transcript;
#                 const streamlitEvent = new CustomEvent("streamlit:message", {
#                     detail: { type: "speech", data: transcript }
#                 });
#                 window.parent.document.dispatchEvent(streamlitEvent);
#             };

#             recognition.onerror = (event) => {
#                 const streamlitEvent = new CustomEvent("streamlit:message", {
#                     detail: { type: "error", data: event.error }
#                 });
#                 window.parent.document.dispatchEvent(streamlitEvent);
#             };
#         };

#         streamlitAudioRecognition();
#         </script>
#         """,
#         height=0,
#         width=0,
#     )

# # Function to handle API response
# def respond(query):
#     st.info("🤖 Thinking...")

#     if "Zara" in query:
#         query = query.replace("Zara", "").strip()

#     payload = {
#         "model": "openai/gpt-4o",
#         "messages": [{"role": "user", "content": f"You are my sweet, smart, knowledgeable, loving, playful, and affectionate AI female friend named Zara. Reply lovingly to this: {query}"}],
#         "max_tokens": 500
#     }

#     headers = {"Authorization": f"Bearer {openrouter_api_key}", "Content-Type": "application/json"}

#     try:
#         response = requests.post(
#             f"{openrouter_api_base}/chat/completions",
#             headers=headers,
#             data=json.dumps(payload),
#             timeout=15
#         )
#         response_data = response.json()

#         if response.status_code == 200 and "choices" in response_data:
#             answer = response_data['choices'][0]['message']['content']
#             messages_array.append({'role': 'assistant', 'content': answer})
#             st.success(f"💬 Zara: {answer}")
#             speak(answer)
#             return answer
#         else:
#             error_message = response_data.get('error', {}).get('message', 'Unknown error')
#             st.error(f"❌ API Error: {error_message}")
#             speak("I'm sorry, there was an issue responding.")

#     except Exception as e:
#         st.error(f"❌ Error contacting OpenRouter API: {e}")
#         speak("There was a connection error.")

# def speak(text):
#     try:
#         clean_old_audio_files()  # Clean before saving new audio
#         tts = gTTS(text=text, lang='en', slow=False, tld='ca')

#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=".") as tmpfile:
#             tts.save(tmpfile.name)
#             tmpfile_path = tmpfile.name

#         # Inject an invisible HTML audio player
#         audio_html = f"""
#         <audio autoplay="true" style="display:none;">
#             <source src="data:audio/mp3;base64,{base64.b64encode(open(tmpfile_path, 'rb').read()).decode()}" type="audio/mp3">
#         </audio>
#         """
#         st.markdown(audio_html, unsafe_allow_html=True)

#         # Clean up the temp file after a short delay
#         time.sleep(5)
#         if os.path.exists(tmpfile_path):
#             os.remove(tmpfile_path)

#     except Exception as e:
#         st.error(f"🎵 Error playing speech: {e}")

# # Add an event listener to capture the transcript returned from JS and pass it to Streamlit
# components.html(
#     """
#     <script>
#     window.parent.document.addEventListener("streamlit:message", function(event) {
#         if (event.detail.type === "speech") {
#             const speech = event.detail.data;
#             window.parent.document.dispatchEvent(new CustomEvent("streamlit:message", {detail: {type: "speechInput", data: speech}}));
#         }
#     });
#     </script>
#     """,
#     height=0,
#     width=0,
# )

# # Capture the speech input and trigger the response
# speech_input = st.session_state.get("speech_input", None)

# if speech_input:
#     st.success(f"🗣️ You said: {speech_input}")
#     messages_array.append({'role': 'user', 'content': speech_input})
#     respond(speech_input)
# else:
#     pass






# # Button to start listening
# if st.button('🎤 Start Talking'):
#     listen()



















import streamlit as st
from gtts import gTTS
import os
import json
import tempfile
import requests
import time
import base64
import glob
from datetime import datetime, timedelta
from dotenv import load_dotenv
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

# Configure the Streamlit page
st.set_page_config(page_title="Voice Assistant - Zara", layout="centered")

# OpenRouter API Key and Base URL
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_api_base = "https://openrouter.ai/api/v1"

# Title
st.title("🎙️ Jeph's AI Assistant -- Zara")

# Initialize message history
if 'messages_array' not in st.session_state:
    st.session_state.messages_array = [
        {'role': 'system', 'content': 'You are my beautiful AI assistant named Zara'}
    ]

# Function to clean old audio files
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

# Function to handle API response
def respond(query):
    st.info("🤖 Thinking...")

    if "Zara" in query:
        query = query.replace("Zara", "").strip()

    payload = {
        "model": "openai/gpt-4o",
        "messages": st.session_state.messages_array + [
            {
                "role": "user",
                "content": (
                    "You are my sweet, smart, Knowledgeable, loving, playful, and affectionate AI female friend named Zara. "
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
            st.session_state.messages_array.append({'role': 'assistant', 'content': answer})
            st.success(f"💬 Zara: {answer}")
            speak(answer)
            return answer
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

        # Convert audio to base64
        audio_base64 = base64.b64encode(open(tmpfile_path, 'rb').read()).decode()
        
        # Inject an invisible HTML audio player
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        components.html(audio_html, height=0)

        # Clean up the temp file after a short delay
        time.sleep(5)
        if os.path.exists(tmpfile_path):
            os.remove(tmpfile_path)

    except Exception as e:
        st.error(f"🎵 Error playing speech: {e}")

# Speech recognition component
def voice_recognition():
    components.html(
        """
        <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        
        function startListening() {
            recognition.start();
            console.log("Listening...");
        }
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            console.log('Transcript:', transcript);
            window.parent.document.dispatchEvent(
                new CustomEvent('streamlit:setComponentValue', {
                    detail: {value: transcript}
                })
            );
        };
        
        recognition.onerror = function(event) {
            console.error('Recognition error:', event.error);
            window.parent.document.dispatchEvent(
                new CustomEvent('streamlit:setComponentValue', {
                    detail: {value: 'ERROR: ' + event.error}
                })
            );
        };
        
        // Start listening when the component loads
        startListening();
        </script>
        """,
        height=0,
        width=0,
    )



# Main app logic
if st.button('🎤 Start Talking'):
    st.session_state.listening = True
    voice_recognition()

# Check for speech input
if 'listening' in st.session_state and st.session_state.listening:
    speech_input = st.text_input("Speech input", key="speech_input", label_visibility="collapsed")
    
    if speech_input and not speech_input.startswith('ERROR'):
        st.session_state.listening = False
        st.success(f"🗣️ You said: {speech_input}")
        st.session_state.messages_array.append({'role': 'user', 'content': speech_input})
        respond(speech_input)
    elif speech_input and speech_input.startswith('ERROR'):
        st.error(f"❌ Error: {speech_input[7:]}")
        st.session_state.listening = False

# Display conversation history
st.subheader("Conversation History")
for message in st.session_state.messages_array[1:]:  # Skip system message
    if message['role'] == 'user':
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Zara:** {message['content']}")







