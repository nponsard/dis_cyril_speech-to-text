from gtts import gTTS
import os

# Choose the language
language = "fr"


def say(text):

    # Create the gTTS object
    tts = gTTS(text, lang=language, slow=False)

    # Save the speech to a file
    tts.save("speech.mp3")

    # Play the speech
    os.system("mpg123 speech.mp3")
