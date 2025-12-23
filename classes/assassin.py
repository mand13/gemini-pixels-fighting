# assassin.py
"""
This module defines the Assassin class, a subclass of Class

TODO improve description
"""

import random
import logging
from . import Class

class Assassin(Class):
    def __init__(self, team_id, level=logging.INFO):
        super().__init__(team_id, level=level)

    # attack logic default: inherited from Class

    # defend logic default: inherited from Class

    # pick_defender logic: try 3 times, making Assassin less likely to pick allies
    def pick_defender(self, grid, attacker_y, attacker_x):
        """
        Assassin pick defender logic
        """
        pickedEnemy = False
        counter = 0
        num_tries = 3
        while not pickedEnemy and counter < num_tries:
            dy = random.choice([-self.range, 0, 1*self.range])
            dx = random.choice([-self.range, 0, self.range])
            defender_y = (attacker_y + dy) % grid.shape[0]
            defender_x = (attacker_x + dx) % grid.shape[1]
            if grid[defender_y, defender_x] != self.team_id:
                pickedEnemy = True
            counter += 1
        return defender_y, defender_x