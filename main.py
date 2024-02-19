import whisper
import torch
from transformers import (
    BertTokenizer,
    BertModel,
    BertForSequenceClassification,
    BertConfig,
    CamembertModel,
    AutoTokenizer,
    CamembertTokenizer,
)
from torch.nn.functional import softmax
from sklearn.neighbors import NearestNeighbors
import numpy as np

print("loading BERT")


# bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_configuration = BertConfig(output_hidden_states=True)
# bert_model = BertModel.from_pretrained("bert-base-uncased", config=bert_configuration)


# Load camembert
bert_tokenizer = CamembertTokenizer.from_pretrained("camembert/camembert-large")

bert_model = CamembertModel.from_pretrained("camembert/camembert-large")


bert_model.eval()


def get_embedding(text):
    # Tokenize the text and convert to input IDs
    inputs = bert_tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=512,
        padding="max_length",
        return_attention_mask=True,
        return_tensors="pt",  # PyTorch tensors
    )

    # Set the model to evaluation mode to deactivate dropout layers
    bert_model.eval()

    # Forward pass, calculate logit predictions
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.pooler_output


class Phrase:
    def __init__(self, text_list, id):
        self.text_list = text_list
        self.id = id
        self.embeddings = []
        self._calculate_embedding()

    def _calculate_embedding(self):
        self.embeddings = torch.stack([get_embedding(text) for text in self.text_list])

    def get_embedding(self):
        return self.embeddings.mean(dim=0).numpy().squeeze()


# phrases = [
#     Phrase(["Turn on the light", "Activate the lights", "lights on"], 0),
#     Phrase(["Activate the mixer", "Turn on the mixer"], 1),
#     Phrase(["What is the weather", "Tell me the weather"], 2),
#     Phrase(["Play music", "Start the music"], 3),
#     Phrase(["Turn off the light", "Deactivate the lights", "lights off"], 4),
#     Phrase(["Deactivate the mixer", "Turn off the mixer"], 5),
# ]


print("Loading phrases...")

phrases = [
    Phrase(["Allume la lumière", "Active les lumières", "lumière allumée"], 0),
    Phrase(["Active le mixeur", "Allume le mixeur"], 1),
    Phrase(["Quel temps fait-il", "Dis-moi la météo"], 2),
    Phrase(["Joue de la musique", "Commence la musique"], 3),
    Phrase(["Éteins la lumière", "Désactive les lumières", "lumière éteinte"], 4),
    Phrase(["Désactive le mixeur", "Éteins le mixeur"], 5),
]


# Collect embeddings and their labels
X = []  # This will store the embeddings
y = []  # This will store the corresponding ids (labels)

indexes = []

texts = []

for index, phrase in enumerate(phrases):
    # X.append(phrase.get_embedding())  # Get the average embedding for the phrase
    # y.append(phrase.id)  # The id is the label for the embedding

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


print("Loading whisper model...")
whisper_model = whisper.load_model("medium")

print("Transcribing audio...")
result = whisper_model.transcribe("lumiere3.wav")


text = result["text"]
print(f"Transcribe : {text}")

target_embedding = get_embedding(text)
distance, indices = knn.kneighbors(target_embedding)

index = indices[0][0]
print(f"indice: {index}")
print(f"Exact phrase: {texts[index]}")
index = indexes[index]
similarity = 1 - distance[0][0]

print(f"index: {index}")

print(f"Phrase: {phrases[index].text_list[0]}, Similarity: {similarity}")
