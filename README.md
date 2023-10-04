# DungeonsAndDragons
Use the power of LLM's and ChatGPT to play single player Dungeons and Dragons. 
Choose the universe you want to play in (such as Star Wars, Marvel, The Last of Us, or even Original DND) and let your imagination run wild.

This code solves all of the regular pitfalls of using ChatGPT as a dungeon master such as:
 - forgetting earlier events (token limits)
 - handling combat
 - introducing skill checks

This code also allows for save states of your game for continuous campaigns between sessions.

How to use:
Change out the API key with your OpenAI API. You can then run the program, at this point, it will be pretty straight forward on how to play. For your first prompt, give the model the setting you want to play in and your character stats, or have the model come up with this all on its own. If you have a save state in dnd_save.txt then just type "continue" and the model where start where your previous session left off.

Two essential commands you must know are:
- "save": saves the state of your game in dnd_save.txt
- "exit": ends your session
Make sure to save before ending your session.
