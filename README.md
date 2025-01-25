# Prince Adventure Game

## Overview
Prince Adventure is a 2D action game developed using the Kivy framework in Python. The player controls a prince who must navigate through three stages, defeat monsters, and reach the door to advance to the next stage. The game features animations, sound effects, and a timer to add to the challenge.

## Features
- **Three Stages**: Each stage has a unique background and increasing difficulty.
- **Monsters**: Different types of monsters with varying HP, damage, and speed.
- **Timer**: Each stage has a time limit to complete.
- **Sound Effects**: Background music, attack sounds, and door sounds.
- **Health Bar**: The prince has a health bar that decreases when attacked by monsters.
- **Win/Lose Conditions**: The player wins by completing all stages within the time limit and loses if the prince's health reaches zero or time runs out.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/prince-adventure-game.git
   cd prince-adventure-game
   ```

2. **Install dependencies**:
   ```bash
   pip install kivy
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

## Controls
- **W**: Move up
- **A**: Move left
- **S**: Move down
- **D**: Move right
- **G**: Attack

## Gameplay
1. **Stage 1**: Defeat minions and a centaur to reach the door.
2. **Stage 2**: Defeat more minions and centaurs to advance.
3. **Stage 3**: Defeat minions, centaurs, and a boss to win the game.

## File Structure
- `main.py`: The main game logic and classes.
- `game.kv`: The Kivy layout and UI definitions.
- `images/`: Contains all the sprite images for the prince and monsters.
- `sounds/`: Contains all the sound effects and background music.

## Screenshots
![Menu Screen](images/background/startgame.png)
![Stage 1](images/background/cave.jpg)
![Stage 2](images/background/stage2.jpg)
![Stage 3](images/background/stage3.jpg)

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Acknowledgments
-Kivy Framework: The framework used to build this game.
-Sound Effects: Sound effects are sourced from Mixkit.
-Sprite Images: Character sprites are from Action RPG Character Pack by Fraanco.

## Contact
For any questions or feedback, please contact teeranonn124@gmail.com.

---

Enjoy the game and good luck on your adventure! 🎮