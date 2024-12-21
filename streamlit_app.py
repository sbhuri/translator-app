import streamlit as st
from gtts import gTTS
import openai
import os
from PyPDF2 import PdfReader
import pandas as pd

openai.api_key = os.ENV("API_Token")
def translate_text(text, target_language):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful language translator."},
                {"role": "user", "content": f"Translate this text to {target_language}: {text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

def convert_text_to_speech(text, language_code):
    try:
        tts = gTTS(text=text, lang=language_code)
        audio_file = "output.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None


def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"PDF extraction error: {e}")
        return None

def extract_text_from_file(file):
    try:
        if file.name.endswith('.txt'):
            return file.read().decode("utf-8")
        else:
            st.error("Unsupported file format. Please upload a TXT or PDF file.")
            return None
    except Exception as e:
        st.error(f"File extraction error: {e}")
        return None


st.title("Language Translator and Text-to-Speech Converter")
st.write("Translate english text into various languages and convert it into speech.")


input_method = st.radio("Choose input method", ("Enter text", "Upload file"))

if input_method == "Enter text":
    user_text = st.text_area("Enter your text here")
else:
    uploaded_file = st.file_uploader("Upload a file (TXT, CSV, XLSX, PDF)")
    if uploaded_file:
        if uploaded_file.name.endswith('.pdf'):
            user_text = extract_text_from_pdf(uploaded_file)
        else:
            user_text = extract_text_from_file(uploaded_file)

languages = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Bengali": "bn",
    "Hindi": "hi",
    "Telugu": "te",
    "Japanese": "ja",
    "Korean": "ko"
}
target_language = st.selectbox("Select target language", list(languages.keys()))


if st.button("Translate and Convert to Speech"):
    if not user_text:
        st.error("Please provide some text or upload a file.")
    else:
        # Translate the text
        translated_text = translate_text(user_text, target_language)
        if translated_text:
            st.success("Translation successful!")
            st.write(translated_text)

            # Convert the translated text to speech
            audio_file = convert_text_to_speech(translated_text, languages[target_language])
            if audio_file:
                st.audio(audio_file, format="audio/mp3")
                with open(audio_file, "rb") as file:
                    st.download_button(
                        label="Download Audio",
                        data=file,
                        file_name="translated_speech.mp3",
                        mime="audio/mp3"
                    )
                # Remove the temporary audio file
                os.remove(audio_file)
