# Prince Adventure Game

## Overview
Prince Adventure is a 2D action game developed using the **Kivy** framework in Python. The player controls a prince who must navigate through three stages, defeat monsters, and reach the door to advance to the next stage. The game features animations, sound effects, a timer, and a health system to increase the challenge.

---

## Features
- **Three Stages**: Each stage has a unique background and increasing difficulty.
- **Monsters**: Different types of monsters with varying HP, damage, and speed.
- **Timer**: Each stage has a time limit to complete.
- **Sound Effects**: Background music, attack sounds, and door sounds.
- **Health Bar**: The prince has a health bar that decreases when attacked by monsters.
- **Win/Lose Conditions**: The player wins by completing all stages within the time limit and loses if the prince's health reaches zero or time runs out.

---

## Code Explanation

### 1. **Program Structure**
The program is divided into two main parts:
- **main.py**: The main file containing the game logic and classes such as characters, monsters, and game systems.
- **game.kv**: The file containing UI design and layout using Kivy Language.

---

### 2. **Main Classes and Functions**

#### **Door**
- **Purpose**: Checks collision with the prince and transitions to the next stage when the prince stays on the door for 3 seconds.
- **Key Methods**:
  - `check_collision`: Checks collision between the prince and the door.
  - `next_stage`: Transitions to the next stage.

#### **Prince**
- **Purpose**: Controls the prince's movement, attacks, and health.
- **Key Methods**:
  - `move_step`: Moves the prince based on key presses.
  - `take_damage`: Reduces health when attacked.
  - `update_animation`: Updates movement and attack animations.
  - `play_sword_sound`, `play_hurt_sound`: Plays sounds for attacks and taking damage.

#### **MonsterBase**
- **Purpose**: The base class for all monsters.
- **Key Methods**:
  - `update_position`: Updates the monster's position.
  - `take_damage`: Reduces health when attacked.
  - `attack_prince`: Attacks the prince on collision.

#### **Minion, Centaur, Boss**
- **Purpose**: Different types of monsters inheriting from `MonsterBase`, each with unique HP, damage, and speed.

#### **GameScreen, GameScreenTwo, GameScreenThree**
- **Purpose**: Screens for each stage.
- **Key Methods**:
  - `start_timer`: Starts the timer.
  - `update_timer`: Updates the remaining time.
  - `end_game`: Ends the game when time runs out or the prince's health reaches 0.

#### **GameOver, GameWin**
- **Purpose**: Screens displayed when the player loses or wins the game.

---

### 3. **Game Systems**

#### **Movement**
- The player uses `W`, `A`, `S`, `D` keys to control the prince.
- Movement is handled in the `move_step` method of the `Prince` class.

#### **Attacks**
- Press `G` to attack.
- Attacks are handled in the `move_step` method of the `Prince` class.

#### **Collision**
- The system checks for collisions between the prince and monsters or the door using the `collides` function in the `Door` class.

#### **Timer**
- Each stage has a time limit. If the time runs out, the player loses.
- The timer is managed in the `update_timer` method of the `BaseGameScreen` class.

#### **Health**
- The prince's health decreases when attacked. If health reaches 0, the player loses.
- Health is managed in the `take_damage` method of the `Prince` class.

---

### 4. **Sound Effects**
- Background music for each stage.
- Button click sounds.
- Attack and damage sounds.
- Door opening sounds.

---

## How to Run the Program

### 1. **Set Up the Environment**
- Install Python version 3.7 or higher.
- Install Kivy using the command:
  ```bash
  pip install kivy
  ```

### 2. **Download the Project**
- Clone the repository:
  ```bash
  git clone https://github.com/teeranon124/gameprince.git
  cd gameprince
  ```

### 3. **Run the Program**
- Run the `main.py` file:
  ```bash
  python main.py
  ```

---

## How to Play
1. **Start the Game**: Click "Start Game" on the menu screen.
2. **Control the Prince**:
   - `W`: Move up
   - `A`: Move left
   - `S`: Move down
   - `D`: Move right
   - `G`: Attack
3. **Clear the Stage**: Defeat monsters and reach the door within the time limit.
4. **Win the Game**: Complete all 3 stages to win.

---

## File Structure
- `main.py`: The main game logic and classes.
- `game.kv`: The Kivy layout and UI definitions.
- `images/`: Contains all the sprite images for the prince and monsters.
- `sounds/`: Contains all the sound effects and background music.

---

## Screenshots
![Menu Screen](images/background/startgame.png)
![Stage 1](images/background/cave.jpg)
![Stage 2](images/background/stage2.jpg)
![Stage 3](images/background/stage3.jpg)

---

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

## Acknowledgments
- **Kivy Framework**: The framework used to build this game.
- **Sound Effects**: Sound effects are sourced from [Mixkit](https://mixkit.co/free-sound-effects).
- **Sprite Images**: Character sprites are from [Action RPG Character Pack by Fraanco](https://fraanco.itch.io/action-rpg-character?download).

---

## Contact
For any questions or feedback, please contact [teeranonn124@gmail.com](mailto:teeranonn124@gmail.com).

---

Enjoy the game and good luck on your adventure! 🎮

---
