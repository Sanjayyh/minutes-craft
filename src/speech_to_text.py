from faster_whisper import WhisperModel
import subprocess
from pathlib import Path

# =========================================
# LOAD MODEL ONCE
# =========================================

print("\n===== LOADING FASTER WHISPER MODEL =====\n")

model = WhisperModel(
    "medium",           # small = fast + good accuracy
    device="cpu",      # use cpu
    compute_type="int8"  # optimized for cpu
)

print("\n===== MODEL LOADED =====\n")


# =========================================
# CONVERT AUDIO TO WAV
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

# =========================================
# TRANSCRIBE FUNCTION
# =========================================

def transcribe_media(file_path: Path) -> str:

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found")

    wav_path = file_path.with_suffix(".wav")

    print("\n===== CONVERTING AUDIO =====\n")

    convert_to_wav(file_path, wav_path)

    print("\n===== STARTING TRANSCRIPTION =====\n")

    segments, info = model.transcribe(
    str(wav_path)
)

    print("Detected language:", info.language)

    print("\n===== DETECTED LANGUAGE =====\n")
    print(info.language)

    transcript = ""

    for segment in segments:

        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

        transcript += segment.text + " "

    print("\n===== FINAL TRANSCRIPT =====\n")

    print(transcript)

    print("\n===== TRANSCRIPTION COMPLETED =====\n")

    return transcript.strip()