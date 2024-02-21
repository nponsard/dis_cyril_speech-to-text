from embedding import get_embedding


from intent import find_neighbor
from recognise import recognise_action_voice
from train import load_training
from transcribe import transcribe
from train import TrainingData

treshold = 0.931


knn, texts, indexes, phrases = load_training()


file = "lumiere.wav"

print(
    recognise_action_voice(file, TrainingData(knn, texts, indexes, phrases), treshold)
)
