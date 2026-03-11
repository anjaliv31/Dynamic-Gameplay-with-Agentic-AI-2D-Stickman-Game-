# 🎮 Dynamic Gameplay with Agentic AI (2D Stickman Game)

A **2D Stickman Shooting Game** built using **Python and PyGame** where an AI opponent learns gameplay strategies using **Reinforcement Learning (Q-Learning)**.

The project demonstrates how **agentic AI systems can adapt to player actions** and improve their behavior over time through reward-based learning.

---

## 🚀 Features

* 🎯 **Adaptive AI Opponent** using Q-Learning
* 🧠 **Reinforcement Learning based decision making**
* 🎮 **Interactive 2D Gameplay using PyGame**
* 🧩 Modular game architecture
* 💣 Strategic gameplay with enemies and bombs
* 📊 AI learns from player actions and improves over time

---

## 🧠 How the AI Works

The AI agent uses **Q-Learning**, a reinforcement learning technique, to decide where to shoot.

Steps:

1. The AI observes the **current game state**.
2. It chooses an **action (shoot location)** using exploration or exploitation.
3. The AI receives a **reward or penalty** based on the result.
4. The **Q-table updates**, improving future decisions.

Over time, the AI learns better shooting strategies.

---

## 🛠 Tech Stack

| Technology             | Purpose                      |
| ---------------------- | ---------------------------- |
| Python                 | Core programming language    |
| PyGame                 | 2D game development          |
| Reinforcement Learning | Adaptive AI behavior         |
| Q-Learning             | AI decision-making model     |
| Flask                  | Optional backend integration |

---

## 📂 Project Structure

```
stickman-agentic-ai-game
│
├── main.py                     # Main game loop
├── game_logic.py               # Core gameplay logic
├── ui.py                       # Game UI rendering
├── reinforcement_learning.py   # Q-learning algorithm
├── q_table.json                # AI learned data
├── requirements.txt            # Project dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```
git clone https://github.com/yourusername/stickman-agentic-ai-game.git
```

Move to project directory:

```
cd stickman-agentic-ai-game
```

Create virtual environment:

```
python -m venv venv
```

Activate environment:

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## ▶️ Run the Game

```
python main.py
```

---

## 🎮 Gameplay

1. Place **enemies and bombs on the grid**
2. Shoot enemies while **avoiding bombs**
3. If a bomb is hit, **AI wins**
4. The AI **learns from gameplay patterns**

---

## 📚 Skills Demonstrated

* Reinforcement Learning Fundamentals
* Game Development using PyGame
* AI Decision Making Systems
* Debugging and Performance Optimization
* Python Modular Architecture

---

## 🔮 Future Improvements

* Deep Reinforcement Learning (DQN)
* Multiplayer gameplay
* Difficulty levels
* Better AI training system
* Game analytics dashboard

---

## 👩‍💻 Author

**Mythri Krishna**
CSE – Artificial Intelligence & Machine Learning
VidyaVardhaka College of Engineering

---

⭐ If you like this project, consider giving it a star!
