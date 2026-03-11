import json
from collections import defaultdict
import random

class QLearning:
    def __init__(self):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.learning_rate = 0.5
        self.discount_factor = 0.95
        self.exploration_rate = 0.1

    def choose_action(self, state):
        if random.random() < self.exploration_rate:
            # Exploration: choose random action
            return random.randint(0, 4) * 160 + 80, random.randint(0, 2) * 100 + 100  # Random target in grid
        else:
            # Exploitation: choose best action based on Q-values
            best_action = max(self.q_table[state], key=self.q_table[state].get, default=None)
            if best_action is not None:
                return best_action
            else:
                return random.randint(0, 4) * 160 + 80, random.randint(0, 2) * 100 + 100  # Random target in grid

    def record_state_action(self, state, action, reward):
        old_q_value = self.q_table[state][action]
        new_q_value = old_q_value + self.learning_rate * (reward + self.discount_factor * max(self.q_table[state].values(), default=0) - old_q_value)
        self.q_table[state][action] = new_q_value

    def save_q_table(self):
        q_dict = {str(state): {str(action): value for action, value in actions.items()} for state, actions in self.q_table.items()}
        with open('q_table.json', 'w') as f:
            json.dump(q_dict, f)

    def load_q_table(self):
        try:
            with open('q_table.json', 'r') as f:
                q_dict = json.load(f)
            self.q_table = defaultdict(lambda: defaultdict(float))
            for state_str, actions in q_dict.items():
                state = eval(state_str)
                for action_str, value in actions.items():
                    action = eval(action_str)
                    self.q_table[state][action] = value
        except FileNotFoundError:
            pass
