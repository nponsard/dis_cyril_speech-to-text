from embedding import get_embedding


from intent import find_neighbor
from train import load_training
from transcribe import transcribe
from train import TrainingData

treshold = 0.931


knn, texts, indexes, phrases = load_training()


file = "lumiere.wav"

text = transcribe(file)


while text != "stop":
    text = input("Enter a command: ")

    target_embedding = get_embedding(text)
    index, similarity = find_neighbor(knn, target_embedding, indexes)
    print(f"index: {index}")

    print(f"Phrase: {phrases[index].text_list[0]}, Similarity: {similarity}")
