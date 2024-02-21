import torch
import torchaudio
from transformers import (
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
)

model_name = "Ilyes/wav2vec2-large-xlsr-53-french"
device = "cpu"

model = Wav2Vec2ForCTC.from_pretrained(model_name).to(device)
processor = Wav2Vec2Processor.from_pretrained(model_name)
# resampler = torchaudio.transforms.Resample(48_000, 16_000)


def transcribe(file_path):
    # Load the audio file and resample it to 16kHz
    speech, _ = torchaudio.load(file_path)
    # speech = resampler.forward(speech.squeeze(0)).numpy()
    # sampling_rate = resampler.new_freq

    sampling_rate = 16_000

    # Use the model to transcribe the speech
    features = processor(
        speech.squeeze(0), sampling_rate=sampling_rate, padding=True, return_tensors="pt"
    )
    input_values = features.input_values.to(device)
    attention_mask = features.attention_mask.to(device)
    with torch.no_grad():
        logits = model(input_values, attention_mask=attention_mask).logits
    pred_ids = torch.argmax(logits, dim=-1)

    # Return the transcription
    return processor.batch_decode(pred_ids)[0]
