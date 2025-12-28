# plague.py
"""
This module defines the Plague class, a subclass of Class

TODO improve description
"""

import random
import logging
from . import Class

class Plague(Class):
    def __init__(self, team_id, level=logging.INFO):
        super().__init__(team_id, level=level)
        self.spread_chance = 0.6  # chance to spread after a successful attack

    def attack(self, grid, attacker_y, attacker_x, defender, defender_y, defender_x):
        """
        Default attack logic
        """
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} attacks from ({attacker_y}, {attacker_x}) to team {defender.team_id} at ({defender_y}, {defender_x})")

        # Implement attack mechanics here
        defense = defender.defend(grid, defender_y, defender_x, self, attacker_y, attacker_x)
        if defense == 0: # Defense failed, capture the pixel
            grid[defender_y, defender_x] = self.team_id
            self.logger.debug(f"Pixel at ({defender_y}, {defender_x}) captured by team {self.team_id} ({self.__class__.__name__})")
            if random.random() < self.spread_chance:
                # Attempt to spread to a neighboring pixel
                new_defender_y, new_defender_x = self.pick_defender(grid, defender_y, defender_x)
                new_defender = 
                self.attack(grid, defender_y, defender_x, TODO_defender, new_defender_y, new_defender_x)
            return 1 # Attack successful
        elif defense == 1: # Defense successful, no capture
            self.logger.debug(f"Pixel at ({defender_y}, {defender_x}) defended by team {defender.team_id} ({defender.__class__.__name__})")
            return 0 # Attack failed
        else:
            self.logger.error("Invalid defense return value")
            return -1 # Error
     

    # defend logic default: inherited from Class

    # pick_defender logic default: inherited from Class