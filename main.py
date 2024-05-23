from time import sleep

import requests
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


grobuzin_url = "http://192.168.122.199:8080"

responses = {
    "ligth_on": "Okay, j'allume la lumière",
    "mixer_on": "Okay, j'allume le mixeur",
    "weather": "Je n'a pas accès à la météo pour le moment",
    "music": "Okay, je lance la musique",
    "light_off": "Okay, j'éteins la lumière",
    "mixer_off": "Okay, j'éteins le mixeur",
}

ids = {
    "bonjour" : "eb963dd2-1c81-4c82-8e2d-239c613dee96"
}

not_understood = "Désolé, je n'ai pas compris"

while True:
    print("Recording next...")
    record_voice()
    print("Finished recording.")
    print("Getting action...")
    action = recognise_action_voice(file, training_data, treshold)
    text = not_understood
    if action is not None:
        text = requests.post(grobuzin_url+"/function/"+ids[action]+"/run").json()["message"]
    print(text)
    say(text)
    sleep(1)
