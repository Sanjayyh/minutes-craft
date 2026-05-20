from flask import Flask, request, jsonify, render_template, send_from_directory
from pathlib import Path
from werkzeug.utils import secure_filename

from speech_to_text import transcribe_media
from minutes_generator import process_minutes

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STATUS_FILE = DATA_DIR / "status.txt"

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status")
def get_status():

    if STATUS_FILE.exists():

        return jsonify({
            "status": STATUS_FILE.read_text(
                encoding="utf-8"
            )
        })

    return jsonify({
        "status": ""
    })

@app.route("/transcribe", methods=["POST"])
def transcribe():

    try:

        if "audio" not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400

        file = request.files["audio"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Secure filename
        filename = secure_filename(file.filename)

        filepath = DATA_DIR / filename

        file.save(filepath)

        print("Audio saved:", filepath)



        # Delete old transcript if exists
        transcript_file = DATA_DIR / "auto_minutes.txt"

        if transcript_file.exists():
            transcript_file.unlink()

        # Transcribe
        transcript = transcribe_media(filepath)

        print("\n===== TRANSCRIPT RECEIVED =====\n")
        print(transcript[:1000])

        # Save transcript
        transcript_file.write_text(
            transcript,
            encoding="utf-8"
        )

        return jsonify({
            "message": "Transcription successful",
            "transcript": transcript
        })

    except Exception as e:

        print("Transcription Error:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/generate", methods=["POST"])
def generate():

    try:

        transcript_file = DATA_DIR / "auto_minutes.txt"

        if not transcript_file.exists():

            return jsonify({
                "error": "Transcript not found. Please transcribe audio first."
            }), 400

        result_files = process_minutes()

        return jsonify({
            "message": "Minutes generated successfully",
            "files": result_files
        })

    except Exception as e:

        print("Generation Error:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/data/<filename>")
def download(filename):

    return send_from_directory(
        DATA_DIR,
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)