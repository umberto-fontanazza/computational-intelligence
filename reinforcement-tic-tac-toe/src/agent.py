from typing import Callable
from src.state import State, Action, Quality
from dataclasses import dataclass, field
from random import shuffle, random, choice
from queue import LifoQueue

𝛄 = .8
α = .5
q_initial = 0

@dataclass()
class Agent():
    q_table : dict[tuple[State, Action], Quality] = field(default_factory = dict)
    pending_q_updates: LifoQueue[tuple[State, Action, Quality, State | None]] = LifoQueue() # Sₜ, Aₜ, Rₜ, Sₜ₊₁
    last_choice: tuple[State, Action] | None = None

    def update_q_table(self) -> None:
        """Updates the q_table for a single game, starting from the end of the game and going back for a faster learning"""
        while(not self.pending_q_updates.empty()):
            state, action, reward, res_state = self.pending_q_updates.get()
            # retreive old_q
            if (state, action) in self.q_table:
                old_q = self.q_table[state, action]
            else:
                old_q = 0
            # compute future q
            if not res_state:
                q_expectation = 0
            else:
                q_expectation = max([self.q_table[res_state, act] if (res_state, act) in self.q_table else 0 for act in res_state.actions])
            new_q = (1 - α) * old_q + α * (reward + 𝛄 * q_expectation)
            self.q_table[state, action] = new_q

    def move(self, state: State, epsilon: float | None = None) -> Action:
        """Epsilon is the chance to make a random move, otherwise the move with the best expected quality
        is selected. If more actions have the same q a random choice is performed between the best qs."""
        actions = state.actions
        if epsilon and random() < epsilon:
            return choice(actions)
        q: list[Quality] = [self.q_table[state, action] if (state, action) in self.q_table else q_initial for action in actions]
        actions_q: list[tuple[Action, Quality]] = list(zip(actions, q))
        shuffle(actions_q)
        best_action: Action = max(actions_q, key = lambda t: t[1])[0]
        self.last_choice = state, best_action
        return best_action

    def input(self, new_state: State | None, reward: Quality):
        """Takes input from environment, if game is not over marks the taken choice as to be updated,
        if the game is over makes all the updates stacked up so far"""
        if self.last_choice:
            state, action = self.last_choice
            self.pending_q_updates.put((state, action, reward, new_state))
        if not new_state:
            self.update_q_table()
            self.reset()

    @property
    def policy(self) -> Callable[[State], Action]:
        return lambda s: self.move(s)

    def reset(self):
        self.pending_q_updates = LifoQueue()
        self.last_choice = None