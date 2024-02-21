import torch

from embedding import get_embedding


class Phrase:
    def __init__(self, text_list, id):
        # put to lowercase
        self.text_list = text_list
        self._calculate_embedding()
        self.id = id

    def _calculate_embedding(self):
        self.embeddings = torch.stack([get_embedding(text) for text in self.text_list])

    def get_embedding(self):
        return self.embeddings.mean(dim=0).numpy().squeeze()
