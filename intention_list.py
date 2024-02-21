from phrase import Phrase


texts = [
    ["Allume la lumière", "Active les lumières", "lumière allumée"],
    ["Active le mixeur", "Allume le mixeur"],
    ["Quel temps fait-il", "Dis-moi la météo"],
    ["Joue de la musique", "Commence la musique"],
    ["Éteint la lumière", "Désactive les lumières", "lumière éteinte", "éteins la lumière"],
    ["Désactive le mixeur", "Éteins le mixeur"],
]


def get_phrases():
    print("Loading phrases...")
    phrases = []
    for text_list in texts:
        phrases.append(Phrase(text_list))
    return phrases
