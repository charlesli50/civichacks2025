import os
import speech_recognition as sr
import nltk
from openai import OpenAI
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize
import pandas as pd

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
            {"role": "system", "content": "You are an AI that evaluates school district performance. You will be provided with text transcriptions from the students."},
            {"role": "user", "content": f"Generate a summary of what the students are saying about the school district:\n{text}"}
        ]
    )
    return response.choices[0].message

def summarize_text_audio_transcription(df):
    all_transcriptions = " ".join(df["text_audio_transcription"])
    summary = summarize_text(all_transcriptions)
    return summary.content


if __name__ == '__main__':
    print("hi!")
    # text = transcribe_audio()
    # print("Transcribed Text:")
    # print(text)
    # print("\nSummarized Text:")
    # print(summarize_text(text).content)

    df = pd.read_csv('./fake_survey_data.csv')

    summary = summarize_text_audio_transcription(df)
    print(summary)