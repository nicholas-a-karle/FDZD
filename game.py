
import dialogueparser

# Game contains 4 boxes
# Conversations are logged as part of these 4 boxes based on the last note
box_notes = [
    "!box 1", "!box 2", "!box 3", "!box 4"
]

# files to load into game
files = [

]

conversation_boxes = [
    [], [], [], []
]


if __name__== "__main__":
    for file in files:
        file_conversation = dialogueparser.process(file)
        note = file_conversation.note
        for i in range(len(box_notes)):
            if note == box_notes[i]:
                conversation_boxes[i].append(file_conversation)
                break # break out of inner loop
    
    # conversations loaded into boxes