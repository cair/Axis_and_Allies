import random

import numpy as np

from axis_and_allies.interface import Interface
from axis_and_allies.game import Game
from axis_and_allies.bot import Bot
from axis_and_allies.modified_bot import NewBot2


class ReinforcementBot(NewBot2):
    def __init__(self):
        super().__init__()
        self.interface = Interface()
        self.selected_unit = None
        self.q_table = {}
        self.eps = 0.0001
        self.actions = [for i in range(9)]

    def q(self, state, action=None):

        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))

        if action is None:
            return self.q_table[state]

        return self.q_table[state][action]


    def choose_action(self, state):
        if random.uniform(0, 1) < self.eps:
            return random.choice(self.actions)
        else:
            return np.argmax(self.q(state))

    def act(self, n: int, game):
        if n == 0:
            self.interface.select_inf(game)
        elif n == 1:
            self.interface.select_tank(game)
        elif n == 2:
            self.interface.move_down(game, self.selected_unit)
        elif n == 3:
            self.interface.move_up(game, self.selected_unit)
        elif n == 4:
            self.interface.move_left(game, self.selected_unit)
        elif n == 5:
            self.interface.move_right(game, self.selected_unit)
        elif n == 6:
            self.interface.next_phase(game)
        elif n == 7:
            self.interface.purchase_inf(game)
        elif n == 8:
            self.interface.purchase_tank(game)

    def run(self, start_state):
        N_EPISODES = 100
        MAX_EPISODE_STEPS = 100

        for e in range(N_EPISODES):

            state = start_state
            total_reward = 0
            alpha = alphas[e]

            for _ in range(MAX_EPISODE_STEPS):
                action = self.choose_action(state)
                next_state, reward, done = self.act(state, action)
                total_reward += reward

                q(state)[action] = q(state, action) + \
                                   alpha * (reward + gamma * np.max(q(next_state)) - q(state, action))
                state = next_state
                if done:
                    break