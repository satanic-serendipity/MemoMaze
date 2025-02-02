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
![Start Screen](screenshots/start_screen.png)

### Screenshot 2: Top View of the Maze (before transformation)
![Top View](screenshots/top_view.png)

### Screenshot 3: First-Person View of the Maze
![First-Person View](screenshots/first_person_view.png)

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
