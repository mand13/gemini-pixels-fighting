# mortar.py
"""
This module defines the Mortar class, a subclass of Class

TODO improve description
"""

import random
import logging
from . import Class

class Mortar(Class): # TODO actually implement this class
    def __init__(self, team_id, color, level=logging.INFO):
        super().__init__(team_id, color, level=level)
        self.range = 10  # Mortar has a longer range
        self.miss_chance = 0.79  # chance to misfire

    def attack(self, grid, attacker_y, attacker_x):
        """
        Mortar attack logic TODO improve description
        """
        if random.random() < self.miss_chance:
            self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} misfired from ({attacker_y}, {attacker_x})")
            return 0 # Attack failed due to misfire

        defender_y, defender_x = self.pick_defender(grid, attacker_y, attacker_x)
        defender = grid[defender_y, defender_x]

        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} attacks from ({attacker_y}, {attacker_x}) to team {defender.team_id} at ({defender_y}, {defender_x})")

        defense = defender.defend(grid, defender_y, defender_x, self, attacker_y, attacker_x)
        if defense == 0: # Defense failed, capture the pixel and a cross around it
            for da in range(-1, 2):
                y = (defender_y + da) % grid.shape[0]
                x = defender_x
                grid[y, x] = self
            for da in [-1, 1]: # don't capture center pixel twice
                y = defender_y
                x = (defender_x + da) % grid.shape[1]
                grid[y, x] = self
            self.logger.debug(f"Pixels at ({defender_y} +\- 1, {defender_x} +\- 1) captured by team {self.team_id} ({self.__class__.__name__})")
            return 1 # Attack successful
        elif defense == 1: # Defense successful, no capture
            self.logger.debug(f"Pixel at ({defender_y}, {defender_x}) defended by team {defender.team_id} ({defender.__class__.__name__})")
            return 0 # Attack failed
        else:
            self.logger.error("Invalid defense return value")
            return -1 # Error

    # defend logic default: inherited from Class

    # pick_defender logic default: inherited from Class