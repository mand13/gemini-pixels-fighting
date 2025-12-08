# berserker.py
"""
This module defines the Berserker class, a subclass of Class, which implements specific attack and defend mechanics for the Berserker team in the game.
"""

import random
import logging
from classes import Class

class Berserker(Class):
    def __init__(self, team_id, level=logging.INFO):
        super().__init__(team_id, level=level)

    def attack(self, grid, attacker_y, attacker_x, defender, defender_y, defender_x):
        """
        Berserker-specific attack logic

        The Berserker attacks a single pixel and converts a cluster of the defender's adjacent allies to Berserker's team.
        """
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} attacks from ({attacker_y}, {attacker_x}) to team {defender.team_id} at ({defender_y}, {defender_x})")

        # Implement specific attack mechanics here
        defense = defender.defend(grid, defender_y, defender_x, self, attacker_y, attacker_x)
        if defense == 0: # Defense failed, capture the pixel
            # attack converts cluster of defender's allies to Berserker's team
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny = (defender_y + dy) % grid.shape[0]
                    nx = (defender_x + dx) % grid.shape[1]
                    if grid[ny, nx] == defender.team_id:
                        # random chance of taking over defender and neighboring allies
                        if random.random() < 0.3:
                            grid[ny, nx] = self.team_id
                            self.logger.debug(f"Pixel at ({ny}, {nx}) captured by team {self.team_id} ({self.__class__.__name__})")
            return 1 # Attack successful
        elif defense == 1: # Defense successful, no capture
            self.logger.debug(f"Pixel at ({defender_y}, {defender_x}) defended by team {defender.team_id} ({defender.__class__.__name__})")
            return 0 # Attack failed
        else:
            self.logger.error("Invalid defense return value")
            return -1 # Error

    # defend logic default: inherited from Class