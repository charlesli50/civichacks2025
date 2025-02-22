import os
import speech_recognition as sr
import nltk
from openai import OpenAI
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize

load_dotenv()
UPLOAD_FOLDER = "uploads"

client = OpenAI()
api_key = os.getenv('API_KEY')
client.api_key = api_key

def transcribe_audio():
    wav_path = os.path.join(UPLOAD_FOLDER, "recording.wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    text = recognizer.recognize_google(audio_data) 
    return text

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI that summarizes text."},
            {"role": "user", "content": f"Summarize the following text:\n{text}"}
        ]
    )
    return response.choices[0].message

if __name__ == '__main__':
    text = transcribe_audio()
    print("Transcribed Text:")
    print(text)
    print("\nSummarized Text:")
    print(summarize_text(text).content)