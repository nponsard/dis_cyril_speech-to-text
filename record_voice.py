import time
import pyaudio
import webrtcvad
import collections
import wave

# Constants for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30  # supports 10, 20 and 30 (ms)
PADDING_DURATION_MS = 1500  # 1.5 seconds of silence
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)
CHUNK_BYTES = CHUNK_SIZE * 2  # 16-bit audio
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
NUM_WINDOW_CHUNKS = int(240 / CHUNK_DURATION_MS)

# Initialize VAD
vad = webrtcvad.Vad(1)  # set aggressiveness from 0 to 3


# Function to check if a chunk contains speech
def is_speech(data, sample_rate):
    return vad.is_speech(data, sample_rate)


# Record until silence is detected
def record_until_silence(audio, stream):
    print("Recording...")
    stream.start_stream()

    ring_buffer = collections.deque(maxlen=NUM_PADDING_CHUNKS)
    chunk_ring_buffer = collections.deque(maxlen=NUM_PADDING_CHUNKS)

    triggered = False
    voiced_frames = []
    for _ in range(NUM_WINDOW_CHUNKS):
        ring_buffer.append(False)
    last_active = time.time()

    while True:
        chunk = stream.read(CHUNK_SIZE)
        active = is_speech(chunk, RATE)
        ring_buffer.append(active)
        if active:
            last_active = time.time()
        if time.time() - last_active > 1 and triggered:
            break

        if not triggered:
            chunk_ring_buffer.append(chunk)
            ring_buffer_count = sum(1 for x in ring_buffer if x)
            if ring_buffer_count > 0.5 * NUM_WINDOW_CHUNKS:
                triggered = True
                print("Triggered")
                voiced_frames.extend(chunk_ring_buffer)
                ring_buffer.clear()
        else:
            if chunk:
                voiced_frames.append(chunk)
            num_voiced = sum(1 for x in voiced_frames[-NUM_PADDING_CHUNKS:] if x)
            if num_voiced == 0:
                break
            # num_unvoiced = ring_buffer.maxlen - sum(1 for x in ring_buffer)
            # if num_unvoiced > 0.9 * ring_buffer.maxlen:
            #     break
    stream.stop_stream()
    print("Finished recording.")
    print("Voiced frames: ", len(voiced_frames))
    return b"".join(voiced_frames)


# Save the recorded audio to a WAV file
def save_to_wav(audio_data, filename):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio_data)


# Initialize PyAudio
audio = pyaudio.PyAudio()

# Start the audio stream
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    start=False,
    frames_per_buffer=CHUNK_SIZE,
)


def record_voice():
    audio_data = record_until_silence(audio, stream)
    save_to_wav(audio_data, f"recorded.wav")


def close_stream():
    stream.close()
    audio.terminate()
