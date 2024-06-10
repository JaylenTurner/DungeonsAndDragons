from langchain.llms import Ollama
from crewai import Agent, Task, Crew, Process
import os
import json
import random

# Initialize the LLM
ollama_openhermes = Ollama(model='openhermes')

# Define the game setting and player stats
"""""""""""""""""""""""""""""""""""

    START OF GAME VARIABLES    


"""""""""""""""""""""""""""""""""""
    
file_path = 'game-state.txt'
game_setting = "Star Wars universe"
player_stats = {
    "name": "Luke Skywalker",
    "class": "Jedi",
    "level": 5,
    "strength": 14,
    "dexterity": 16,
    "constitution": 12,
    "intelligence": 10,
    "wisdom": 14,
    "charisma": 18,
    "background": "A young farm boy from Tatooine who discovers his destiny as a Jedi Knight.",
    "inventory": ["Lightsaber", "Blaster", "Jedi Robes"],
    "abilities": ["Force Push", "Mind Trick", "Lightsaber Combat"],
    "modifiers": {
        "strength": 2,
        "dexterity": 3,
        "constitution": 1,
        "intelligence": 0,
        "wisdom": 2,
        "charisma": 4
    }
}

"""""""""""""""""""""""""""""""""""

    END OF GAME VARIBALES   


"""""""""""""""""""""""""""""""""""

# Define the agents
dungeonMaster = Agent(
    role='DungeonMaster',
    goal=f'Develop intricate story arcs and subplots to enhance player immersion in the {game_setting}. Provide descriptive narration to set the scene and mood for each encounter. Introduce NPCs with distinct personalities and motivations to enrich the game world. Respond dynamically to player actions, creating a responsive and living game environment. Balance combat, exploration, and role-playing elements to cater to diverse player preferences.',
    backstory=f'You are a Dungeon Master for a game of Dungeons and Dragons in the {game_setting}. Do not infer or make actions for the player.',
    verbose=True,
    allow_delegation=False,
    llm=ollama_openhermes
)

referee = Agent(
    role='Referee',
    goal='Identify when player actions require skill checks based on game rules. Calculate skill check outcomes using player character stats and relevant modifiers. Clearly communicate the results of skill checks, including successes and failures. Show the math for all dice rolls and modifiers, and ensure fairness in all rolls. Use the phrase "Skill Check Required" explicitly when a skill check is needed and include the skill check requirement "(DC:)" in the response. Dynamically determine the DC based on the task difficulty. Offer guidance on potential next steps or actions players can take following skill check outcomes. Maintain a log of skill checks and outcomes for reference and consistency throughout the game.',
    backstory=f'You are a Referee in the {game_setting}. Do not cheat the dice rolls; fairness is paramount.',
    verbose=True,
    allow_delegation=False,
    llm=ollama_openhermes
)

# Initialize Crew
crew = Crew(agents=[dungeonMaster, referee])

# Function to save game state
def save_game_state(history, player_stats, game_setting, filename=file_path):
    game_state = {
        "history": history,
        "player_stats": player_stats,
        "game_setting": game_setting
    }
    with open(filename, 'w') as file:
        json.dump(game_state, file)

# Function to load game state
def load_game_state(filename=file_path):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {"history": [], "player_stats": {}, "game_setting": ""}

# Dice roll function
def roll_dice(sides=20):
    return random.randint(1, sides)

# Define a function to handle the game loop
def game_loop(history, player_stats, game_setting):
    while True:
        # Dungeon Master creates a scenario
        scenario_task = Task(
            description="Create a new scenario for the players",
            agent=dungeonMaster,
            inputs={"history": history, "player_stats": player_stats, "game_setting": game_setting}  # Pass history, player stats, and game setting to the DM
        )
        scenario = crew.run(scenario_task)
        print("Dungeon Master:", scenario.result)
        history.append({"role": "DungeonMaster", "content": scenario.result})

        # Player makes an action (simulate player input here)
        player_action = input("Player action: ")
        history.append({"role": "Player", "content": player_action})

        # Referee checks if a skill check is needed
        skill_check_task = Task(
            description="Evaluate player action for skill check",
            agent=referee,
            inputs={"history": history, "player_action": player_action, "player_stats": player_stats, "game_setting": game_setting}  # Pass history, player action, player stats, and game setting to the Referee
        )
        skill_check_result = crew.run(skill_check_task)

        if "Skill Check Required" in skill_check_result.result:
            # Determine the type of skill check required and dynamically set DC
            if "Dexterity check" in skill_check_result.result:
                modifier = player_stats["modifiers"]["dexterity"]
            elif "Strength check" in skill_check_result.result:
                modifier = player_stats["modifiers"]["strength"]
            elif "Constitution check" in skill_check_result.result:
                modifier = player_stats["modifiers"]["constitution"]
            elif "Intelligence check" in skill_check_result.result:
                modifier = player_stats["modifiers"]["intelligence"]
            elif "Wisdom check" in skill_check_result.result:
                modifier = player_stats["modifiers"]["wisdom"]
            elif "Charisma check" in skill_check_result.result:
                modifier = player_stats["modifiers"]["charisma"]
            else:
                modifier = 0  # Default modifier if none specified

            # Extract the DC from the referee's result
            dc_start = skill_check_result.result.find("(DC: ") + 5
            dc_end = skill_check_result.result.find(")", dc_start)
            dc = int(skill_check_result.result[dc_start:dc_end])

            dice_roll = roll_dice()
            total = dice_roll + modifier
            pass_fail = "Success" if total >= dc else "Failure"
            skill_check_result.result += f"\nDice Roll: {dice_roll} + Modifier: {modifier} = Total: {total} (DC: {dc}) - {pass_fail}"

        print("Referee:", skill_check_result.result)
        history.append({"role": "Referee", "content": skill_check_result.result})

        # Check if the game should continue or end
        continue_game = input("Continue game? (yes/no): ").strip().lower()
        if continue_game != 'yes':
            save_game = input("Save game state? (yes/no): ").strip().lower()
            if save_game == 'yes':
                save_game_state(history, player_stats, game_setting)
            break

# Starting the game with an option to load the game state
def start_game():
    load_game = input("Load previous game state? (yes/no): ").strip().lower()
    if load_game == 'yes':
        game_state = load_game_state()
        history = game_state["history"]
        player_stats = game_state["player_stats"]
        game_setting = game_state["game_setting"]
    else:
        history = []

    game_loop(history, player_stats, game_setting)

# Start the game
start_game()
