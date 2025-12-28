# bunker.py
"""
This module defines the Bunker class, a subclass of Class

TODO improve description
"""

import random
import logging
from . import Class

class Bunker(Class):
    def __init__(self, team_id, level=logging.INFO):
        super().__init__(team_id, level=level)
        self.defence_chance = 0.5  # chance to successfully defend

    # attack logic default: inherited from Class

    def defend(self, grid, defender_y, defender_x, attacker, attacker_y, attacker_x):
        """
        Bunker-specific defend logic, high chance of defending attacks TODO improve description
        """
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} defends at ({defender_y}, {defender_x}) against attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")

        # Implement defend mechanics here
        if random.random() < self.defence_chance:
            self.logger.debug(f"{self.team_id} successfully defended ({defender_y}, {defender_x}) against an attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")
            return 1  # Defense successful
        else:
            self.logger.debug(f"{self.team_id} failed to defend ({defender_y}, {defender_x}) against an attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")
            return 0  # Default: defense fails

    # pick_defender logic default: inherited from Class