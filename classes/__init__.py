# __init__.py
"""This module defines the Class class which is used to define the mechanics of each team in the game. Each class has unique attributes and methods that dictate how they interact with the game environment and other classes.

By default, the Class class provides basic attack, defend (always fail defense), and pick_defender methods (range of 1) that can be overridden by subclasses to implement specific behaviors for different teams.
"""

import logging
import random

class Class:
    def __init__(self, team_id, level=logging.INFO):
        """
        Initializes a new instance of the Class class.
        """
        self.team_id = team_id
        self.range = 1
        self.logger = logging.getLogger(__name__) # create logger
        self.logger.setLevel(level) # set logging level

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
            return 1 # Attack successful
        elif defense == 1: # Defense successful, no capture
            self.logger.debug(f"Pixel at ({defender_y}, {defender_x}) defended by team {defender.team_id} ({defender.__class__.__name__})")
            return 0 # Attack failed
        else:
            self.logger.error("Invalid defense return value")
            return -1 # Error

    def defend(self, grid, defender_y, defender_x, attacker, attacker_y, attacker_x):
        """
        Default defend logic
        """
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} defends at ({defender_y}, {defender_x}) against attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")

        # Implement defend mechanics here
        return 0  # Default: defense fails

    def pick_defender(self, grid, attacker_y, attacker_x):
        """
        Default pick defender logic
        """
        dy = random.choice([-self.range, 0, 1*self.range])
        dx = random.choice([-self.range, 0, self.range])
        defender_y = (attacker_y + dy) % grid.shape[0]
        defender_x = (attacker_x + dx) % grid.shape[1]
        return defender_y, defender_x
    
    def get_name(self):
        """
        Returns the name of the class
        """
        return self.__class__.__name__


from .sniper import Sniper
from .healer import Healer
from .berserker import Berserker