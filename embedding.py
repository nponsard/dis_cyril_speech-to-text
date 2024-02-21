from transformers import (
    CamembertModel,
    CamembertTokenizer,
)
import torch

# Load camembert
bert_tokenizer = CamembertTokenizer.from_pretrained("camembert/camembert-large")

bert_model = CamembertModel.from_pretrained("camembert/camembert-large")


bert_model.eval()


def get_embedding(text):
    text = text.lower()
    # Tokenize the text and convert to input IDs
    inputs = bert_tokenizer.encode_plus(
        text,
        # add_special_tokens=True,
        max_length=64,
        padding="max_length",
        # return_attention_mask=True,
        return_tensors="pt",  # PyTorch tensors
    )

    # Set the model to evaluation mode to deactivate dropout layers
    bert_model.eval()

    # Forward pass, calculate logit predictions
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.pooler_output
