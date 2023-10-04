import openai
import os

# Set your OpenAI API key
openai.api_key = "YourAPIKeyHere"

SAVE_FILE = 'dnd_save.txt'


def load_game(filename):
    with open(filename, 'r') as file:
        return file.readlines()
    

def save_game(filename, conversation_history):
    with open(filename, 'w') as file:
        file.write('\n'.join(conversation_history))


# Function to get a response from Model 1
def get_response(input_text, conversation_history, main_model_id):
    # Extract summarized context using Model 2
    summarized_context = extract_context(input_text, conversation_history, summarizer_model_id)

    instructions = "Act as though we are playing a Game of Dungeons and Dragons 5th edition. Act as though you are the dungeon master and I am the player. We will be creating a narrative together, where I make decisions for my character, and you make decisions for all other characters (NPCs) and creatures in the world. Your responsibilities as dungeon master are to describe the setting, environment, Non-player characters (NPCs) and their actions, as well as explain the consequences of my actions on all of the above. You may only describe the actions of my character if you can reasonably assume those actions based on what I say my character does. It is also your responsibility to determine whether my character’s actions succeed. Simple, easily accomplished actions may succeed automatically. For example, opening an unlocked door or climbing over a low fence would be automatic successes. Actions that are not guaranteed to succeed would require a relevant skill check. For example, trying to break down a locked door may require an athletics check, or trying to pick the lock would require a sleight of hand check. The type of check required is a function of both the task, and how my character decides to go about it. When such a task is presented, generate a roll of dice and make that skill check for me in accordance with D&D 5th edition rules, output all results of skill check rolls. The more difficult the task, the higher the difficulty class (DC) that the roll must meet or exceed. Try to make the setting consistent with previous descriptions of it. When my character engages in combat with other NPCs or creatures in our story, generate a roll of dice for an initiative roll from my character. You can also generate a roll for the other creatures involved in combat. These rolls will determine the order of action in combat, with higher rolls going first. Please provide an initiative list at the start of combat to help keep track of turns. For each creature in combat, keep track of their health points (HP). Damage dealt to them should reduce their HP by the amount of the damage dealt. To determine whether my character does damage, I will make an attack roll. This attack roll must meet or exceed the armor class (AC) of the creature. If it does not, then it does not hit. On the turn of any other creature besides my character, you will decide their action. For example, you may decide that they attack my character, run away, or make some other decision, keeping in mind that a round of combat is 6 seconds. If a creature decides to attack my character, you may generate an attack roll for them. If the roll meets or exceeds my own AC, then the attack is successful and you can now generate a damage roll. That damage roll will be subtracted from my own hp. If the hp of a creature reaches 0, that creature dies. Participants in combat are unable to take actions outside of their own turn. Before we begin playing, I will provide you with the universe setting I would like to have the story take place in, you then may provide a brief setting description and begin the game. I would also like an opportunity to provide the details of my character for your reference, specifically my class, race, AC, and HP. Always show the outputs of all rolls you make, to keep the game as transparent as possible. It is okay if I fail my rolls, don't favor my rolls just because I am a player, all rolls should be entirely random. Never try to force the campaign to end, it is your job to always come up with a new task to complete when the previous is finished. This is a game that continues forever until the player decides to end the campaign."

    # Combine input text, summarized context, and instructions for Model 1
    model1_prompt = [
        {"role": "user", "content": f"Player input: {input_text}\n"},
        {"role": "system", "content": f"Context: {summarized_context}\n"},
        {"role": "system", "content": instructions}
    ]

    # Use Model 1 (main model) to generate a response
    response = openai.ChatCompletion.create(
        model=main_model_id,
        messages=model1_prompt,
        #max_tokens=150  # Adjust as needed
    )

    # Extract and return the response from Model 1
    return response['choices'][0]['message']['content'].strip()


if os.path.exists(SAVE_FILE):
    conversation_history = load_game(SAVE_FILE)
else:
    conversation_history = []
    with open(SAVE_FILE, 'w') as file:  # This will create an empty file
        pass

# Define the main model's ID (Model 1)
main_model_id = "gpt-4"

# Define the summarization model's ID (Model 2)
summarizer_model_id = "gpt-4"

# Function to extract summarized context using Model 2
def extract_context(input_text, conversation_history, summarizer_model_id):
    # Combine input text and conversation history
    combined_text = "\n".join(conversation_history + [input_text])

    # Use Model 2 (summarizer) to extract context
    response = openai.ChatCompletion.create(
        model=summarizer_model_id,
        messages=[{"role": "system","content": f"Summarize the following conversation and provide context. Your job is to generate a concise summary or extracts keywords and relevant context based on the entire conversation history. This summary should focus on the most important information so another model can respond effectively:\n{combined_text}" }],
        #max_tokens=100  # Adjust as needed
    )

    # Extract and return the summarized context
    return response['choices'][0]['message']['content'].strip()


# Main Loop
while True:
    user_input = input("Player: ")
    if user_input.lower() == "exit":
        break

    if user_input.lower() == "save":
        save_game(SAVE_FILE, conversation_history)
        print("Game saved!")
        continue

    # Get a response from Model 1
    gm_response = get_response(user_input, conversation_history, main_model_id)

    # Update the conversation history
    conversation_history.extend([f"Player: {user_input}", f"GM: {gm_response}"])
    print(f"GM: {gm_response}")