import whisper

print("Loading whisper model...")
whisper_model = whisper.load_model("medium")


def transcribe(audio_path):

    print("Transcribing audio...")
    result = whisper_model.transcribe(audio_path)

    text = result["text"]
    print(f"Transcribe : {text}")
    return text
