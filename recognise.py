from embedding import get_embedding
from intent import find_neighbor
from train import TrainingData
from transcribe_wav2vec import transcribe


def recognise_action_text(text, training_data: TrainingData, treshold=0.93):
    knn = training_data.knn
    indexes = training_data.indexes
    target_embedding = get_embedding(text)
    index, similarity = find_neighbor(knn, target_embedding, indexes)
    print(
        f"index: {index}, similarity: {similarity}"
    )

    if similarity > treshold:
        return index
    else:
        return None


def recognise_action_voice(file, training_data: TrainingData, treshold=0.93):
    transcribed = transcribe(file)
    print(f"Transcribed: {transcribed}")
    return recognise_action_text(transcribed, training_data, treshold)
