from phrase import Phrase


texts = {
    "bonjour": ["Bonjour", "Salut", "Hello", "Hi"],
}


def get_phrases():
    print("Loading phrases...")
    phrases = []
    for key, text_list in texts.items():
        phrases.append(Phrase(text_list, key))
    return phrases
