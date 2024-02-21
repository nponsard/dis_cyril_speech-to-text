from sklearn.neighbors import NearestNeighbors
import numpy as np


def train_knn(phrases):
    # Collect embeddings and their labels
    X = []  # This will store the embeddings
    y = []  # This will store the corresponding ids (labels)

    indexes = []

    texts = []

    for index, phrase in enumerate(phrases):

        for index_e, embedding in enumerate(phrase.embeddings):
            X.append(embedding.numpy().squeeze())
            y.append(index)
            texts.append(phrase.text_list[index_e])
            indexes.append(index)

    # Convert to numpy arrays
    X = np.array(X)
    y = np.array(y)

    print("Training KNN model...")

    knn = NearestNeighbors(n_neighbors=1, metric="cosine")
    knn.fit(X, y)

    return knn, texts, indexes


def find_neighbor(knn, target_embedding, indexes):
    distance, indices = knn.kneighbors(target_embedding)
    index = indices[0][0]
    similarity = 1 - distance[0][0]

    return indexes[index], similarity
