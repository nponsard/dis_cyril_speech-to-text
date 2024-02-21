from intent import train_knn
from intention_list import get_phrases
import pickle


class TrainingData:
    def __init__(self, knn, texts, indexes, phrases):
        self.knn = knn
        self.texts = texts
        self.indexes = indexes
        self.phrases = phrases


def load_training():
    with open("model.pkl", "rb") as file:
        data = pickle.load(file)
        return data


def save_training():
    print("Loading phrases...")
    phrases = get_phrases()
    print("Training KNN model...")
    knn, texts, indexes = train_knn(phrases)
    data = TrainingData(knn, texts, indexes, phrases)
    print("Saving model...")
    with open("model.pkl", "wb") as file:
        pickle.dump(data, file)
    print("Model saved")


if __name__ == "__main__":
    save_training()
