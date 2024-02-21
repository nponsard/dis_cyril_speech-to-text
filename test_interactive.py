from recognise import recognise_action_text
from train import load_training, TrainingData


training_data = load_training()


while True:
    text = input("Enter a sentence: ")

    action = recognise_action_text(text, training_data)

    if action is not None:
        print(f"Action: {action}, {training_data.phrases[action].text_list[0]}")
    else:
        print("Not understood")
