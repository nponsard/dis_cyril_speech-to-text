from embedding import get_embedding
from intent import find_neighbor
from train import TrainingData
from transcribe import transcribe


def recognise_action_text(text, training_data: TrainingData, treshold=0.93):
    knn = training_data.knn
    texts = training_data.texts
    indexes = training_data.indexes
    target_embedding = get_embedding(text)
    index, similarity = find_neighbor(knn, target_embedding, indexes)
    print(f"index: {index}, matched phrase: {texts[index]}, similarity: {similarity}")

    if similarity > treshold:
        return indexes[index]
    else:
        return None


def recognise_action_voice(file, training_data: TrainingData, treshold=0.93):
    return recognise_action_text(transcribe(file), training_data, treshold)
