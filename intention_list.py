from phrase import Phrase


texts = {
    "ferie": ["Quand est le prochain jour férié ?", "Quand est le prochain jour de congé ?", "Férié", "Jour férié", "Jour de congé"],
    "blague": ["Raconte moi une blague", "Dis moi une blague", "Blague"],
}


def get_phrases():
    print("Loading phrases...")
    phrases = []
    for key, text_list in texts.items():
        phrases.append(Phrase(text_list, key))
    return phrases
