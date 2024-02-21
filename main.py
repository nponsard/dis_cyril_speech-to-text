from time import sleep
from embedding import get_embedding


from intent import find_neighbor
from recognise import recognise_action_voice
from record_voice import record_voice
from train import load_training
from train import TrainingData
from tts import say

treshold = 0.931


training_data = load_training()


file = "recorded.wav"

responses = [
    "Okay, j'allume la lumière",
    "Okay, j'allume le mixeur",
    "Je n'a pas accès à la météo pour le moment",
    "Okay, je lance la musique",
    "Okay, j'éteins la lumière",
    "Okay, j'éteins le mixeur",
]

not_understood = "Désolé, je n'ai pas compris"

while True:
    print("Recording next...")
    record_voice()
    print("Finished recording.")
    print("Getting action...")
    action = recognise_action_voice(file, training_data, treshold)
    text = not_understood
    if action is not None:
        text = responses[action]
    print(text)
    say(text)
    sleep(1)
