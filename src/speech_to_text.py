from faster_whisper import WhisperModel
import subprocess
from pathlib import Path

# =========================================
# PATHS
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

STATUS_FILE = DATA_DIR / "status.txt"

# =========================================
# STATUS UPDATE FUNCTION
# =========================================

def update_status(message):

    with open(
        STATUS_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(message + "\n")

# =========================================
# LOAD MODEL
# =========================================

print("\n===== LOADING FASTER WHISPER MODEL =====\n")

model = WhisperModel(
    "medium",
    device="cpu",
    compute_type="int8"
)

print("\n===== MODEL LOADED =====\n")

# =========================================
# CONVERT AUDIO
# =========================================

def convert_to_wav(input_path, output_path):

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(output_path)
    ])

def update_status(message):

    with open(
        STATUS_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(message + "\n")

# =========================================
# TRANSCRIBE
# =========================================

def transcribe_media(file_path: Path) -> str:

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found")


    # Clear old status
    STATUS_FILE.write_text("", encoding="utf-8")

    wav_path = file_path.with_suffix(".wav")

    print("\n===== CONVERTING AUDIO =====\n")

    update_status("Converting audio...")

    convert_to_wav(file_path, wav_path)

    print("\n===== STARTING TRANSCRIPTION =====\n")

    update_status("Starting transcription...")

    segments, info = model.transcribe(
        str(wav_path)
    )

    # Language detection
    # Language detection
    detected_language = info.language

    print("\n===== DETECTED LANGUAGE =====\n")

    print(detected_language)

    update_status(
        f"Detected language: {detected_language}"
    )

    update_status("")

    update_status("Transcribing segments:")

    update_status("")

    transcript = ""
    # Process segments
    for segment in segments:

        segment_text = segment.text.strip()

        log_line = (
            f"[{segment.start:.2f}s -> "
            f"{segment.end:.2f}s] "
            f"{segment_text}"
        )

        print(log_line)

        update_status(log_line)

        transcript += segment_text + " "

    print("\n===== FINAL TRANSCRIPT =====\n")

    print(transcript)

    update_status("\nTranscription completed successfully.")

    print("\n===== TRANSCRIPTION COMPLETED =====\n")

    return transcript.strip()