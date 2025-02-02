# MemoMaze - A Memory Maze Challenge

## 📌 About the Game

**MemoMaze** is an interactive memory-based maze game built using **Pygame**. Players must navigate through a maze while remembering the correct path and avoiding obstacles. The game challenges both memory and navigation skills.

## 🎮 Gameplay

- The player starts at the **entrance of the maze**.
- The goal is to reach the **exit while remembering the correct path**.
- The path will disappear after a certain time, so do remember to memorize!
- Avoid dead ends!
- The game has three difficulties - Easy, Medium, Hard.

## 🕹️ Controls

- **Arrow Keys** - Move up, down, left, and right
- **Spacebar** - Return to the main menu.
- **"I" Key** - Show instructions from the main menu.
- **"M" Key** - Briefly view the map, and permanent mini-map
- **Esc** - Quit the game

## 📌 Problem Statement

**Memory Maze** is a unique take on traditional memory games, where players must not only rely on their memory but also navigate a maze with unpredictable paths. The game combines memory evaluation with maze clearing, offering an exciting challenge. 

### Requirements:
- A random maze is generated at the beginning of the game.
- The player has 10 seconds to memorize a top-down view of the maze.
- After the time is up, the maze transforms into a first-person view, where the player must navigate through the maze to reach the exit.
- The player's time taken to clear the maze determines their score, and high scores are recorded.
- The game features different difficulty levels (Easy, Medium, Hard), with varying time limits for memorizing the maze and separate high scores for each difficulty.

## 🎓 Hackathon Submission

This project was made as a submission to **Code Conflux**, a hackathon held at my college.

## 🔧 Installation & Running the Game

### Prerequisites

Ensure you have **Python 3.x** installed. Then, install **Pygame**:

```bash
pip install pygame
```

## Running The Game
Clone the repository and run the game:
```bash
git clone https://github.com/yourusername/MemoMaze.git
cd MemoMaze
python main.py

```
## 📷 Screenshots

### Screenshot 1: Game Start Screen
![Screenshot 2025-02-02 211945](https://github.com/user-attachments/assets/2d3d8e58-34fc-44c0-9a4f-badf21f60d92)

### Screenshot 2: Instructions
![Screenshot 2025-02-02 212000](https://github.com/user-attachments/assets/59c0cf28-990c-448a-8e60-82670fc9b9d2)

### Screenshot 3: Top View of the Maze 
![Screenshot 2025-02-02 212136](https://github.com/user-attachments/assets/0b6f7e3f-0deb-4313-bd91-9c15001ecf83)

### Screenshot 4: First-Person View of the Maze (Corridor)
![Screenshot 2025-02-02 212301](https://github.com/user-attachments/assets/950ebecf-5aa8-40b4-9d08-c8708834b8a0)

### Screenshot 5: First-Person View of the Maze (Exit):
![Screenshot 2025-02-02 212108](https://github.com/user-attachments/assets/c4f8843d-81d1-496c-9680-bb06e61dd43a)

### Screenshot 6: Game Over Screen
![Screenshot 2025-02-02 212122](https://github.com/user-attachments/assets/4a88fb7c-6e97-407f-b606-0881fe28db2f)

## 📷 Assets Used

- `maze_bg.png` - Maze background
- `maze_exit.jpeg` - Exit icon
- `sky.jpg` - Additional background elements
- `font.ttf` - Custom game font
- `high_scores.json` - Stores previous high scores

## 🛠 Future Improvements

- Adding multiple levels with increasing complexity
- Implementing a timer-based challenge mode
- Sound effects and background music

## 📜 License

This project is licensed under the **MIT License**.

## 🤝 Contributing

Feel free to submit pull requests or report issues in the repository!
