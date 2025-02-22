from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
    file.save(webm_path)

    # Convert WebM to MP3 (or WAV if needed)
    mp3_path = webm_path.replace(".webm", ".wav")
    audio = AudioSegment.from_file(webm_path, format="webm")
    audio.export(mp3_path, format="wav")  # Convert to MP3

    return jsonify({"message": "File uploaded successfully", "filename": mp3_path})

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == '__main__':
    app.run(debug=True)