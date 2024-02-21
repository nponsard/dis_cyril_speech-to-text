import pyttsx3

# Initialize the converter
converter = pyttsx3.init()

# Set properties, here we set the rate of speech
converter.setProperty("rate", 150)  # Speed of speech

# Get available voices
voices = converter.getProperty("voices")

found = False
# Search for a French voice
for voice in voices:
    if "french" in voice.name.lower():
        converter.setProperty("voice", voice.id)
        found = True
        break

if not found:
    print("No French voice found")


def say(text):

    # Convert the text to speech
    converter.say(text)

    # Wait for the speech to finish
    converter.runAndWait()
