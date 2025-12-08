# healer.py
"""
This module defines the Healer class, a subclass of Class, which implements specific attack and defend mechanics for the Healer team in the game.
"""

import random
import logging
from classes import Class

class Healer(Class):
    def __init__(self, team_id, level=logging.INFO):
        super().__init__(team_id, level)
        self.health = 0

    def attack(self, grid, attacker_y, attacker_x, defender, defender_y, defender_x):
        """
        Healer-specific attack logic

        The Healer attacks normally, but if the defender happens to be a member of its own team, it heals its collective instead.
        """
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} attacks from ({attacker_y}, {attacker_x}) to team {defender.team_id} at ({defender_y}, {defender_x})")

        # Implement specific attack mechanics here
        if defender.team_id == self.team_id:
            self.health += 1
            self.logger.debug(f"Pixel at ({defender_y}, {defender_x}) healed by team {self.team_id} ({self.__class__.__name__})")
            return 1 # Attack successful
        else:
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
    
    def defend(self, grid, attacker_y, attacker_x, defender, defender_y, defender_x):
        """
        Healer-specific defend logic

        If the healer's team has health, it uses 1 health to successfully defend. Otherwise, it fails to defend.
        """
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} defends at ({defender_y}, {defender_x}) against attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")

        if self.health > 0:
            self.health -= 1
            self.logger.debug(f"{self.team_id} used 1 health to successfully defend ({defender_y}, {defender_x}) against an attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")
            self.logger.debug(f"{self.team_id} has {self.health} health remaining")
            return 1 # Defense successful
        else:
            self.logger.debug(f"{self.team_id} failed to defend ({defender_y}, {defender_x}) against an attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")
            return 0 # Defense failed
        

