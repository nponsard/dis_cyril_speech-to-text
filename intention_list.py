from phrase import Phrase


texts = {
    "light_on": ["Allume la lumière", "Active les lumières", "lumière allumée"],
    "mixer_on": ["Active le mixeur", "Allume le mixeur"],
    "weather": ["Quel temps fait-il", "Dis-moi la météo"],
    "music": ["Joue de la musique", "Commence la musique"],
    "light_off": [
        "Éteint la lumière",
        "Désactive les lumières",
        "lumière éteinte",
        "éteins la lumière",
    ],
    "mixer_off": ["Désactive le mixeur", "Éteins le mixeur"],
}


def get_phrases():
    print("Loading phrases...")
    phrases = []
    for key, text_list in texts.items():
        phrases.append(Phrase(text_list, key))
    return phrases
