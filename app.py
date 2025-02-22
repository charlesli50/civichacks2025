from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from pydub import AudioSegment
import pandas as pd
from data_processing import transcribe_audio

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

df = pd.read_csv('./fake_survey_data.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["audio"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
        

    # Save WebM file
    webm_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    

    # Convert WebM to MP3 (or WAV if needed)
    mp3_path = webm_path.replace(".webm", ".wav")

    if os.path.exists(webm_path):
        os.remove(webm_path)
    if os.path.exists(mp3_path):
        os.remove(mp3_path)

    file.save(webm_path)

    audio = AudioSegment.from_file(webm_path, format="webm")
    audio.export(mp3_path, format="wav")  # Convert to MP3

    return jsonify({"message": "File uploaded successfully", "filename": mp3_path})

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/submit", methods=["POST"])
def submit_survey():
    try:
        survey_data = {
            "student_id": 7777777,
            "house": 90,
            "grade_level": 6,
            "ethnicity": "latino",
            "esl": 0,
            "teacher_helpfulness": int(request.form.get("q1")),
            "curriculum_rigor": int(request.form.get("q2")),
            "student_interest": int(request.form.get("q3")),
            "peer_encouragement": int(request.form.get("q4")),
            "future_success": int(request.form.get("q5")),
            "school_level": "middle",
            "text_audio_transcription": transcribe_audio()
        }

        
        # Optional: Save data to a CSV
        new_df = pd.DataFrame([survey_data])
        # df.to_csv("survey_responses.csv", mode="a", header=not os.path.exists("survey_responses.csv"), index=False)
        new_df.to_csv("new_fake_survey_data.csv")
        
        return jsonify({"message": "Survey submitted successfully", "data": survey_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port = 5555, debug=True)