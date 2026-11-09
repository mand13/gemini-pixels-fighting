# thorns.py
"""
This module defines the Thorns class, a subclass of Class

TODO improve description
"""

import random
import logging
from . import Class

class Thorns(Class):
    def __init__(self, team_id, color, level=logging.INFO):
        super().__init__(team_id, color, level=level)
        self.reflect_chance = 0.3  # chance to reflect attack back to attacker

    # attack logic default: inherited from Class

    def defend(self, grid, defender_y, defender_x, attacker, attacker_y, attacker_x):
        """
        Thorns-specific defend logic TODO improve description
        """
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} defends at ({defender_y}, {defender_x}) against attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")

        if random.random() < self.reflect_chance:
            self.logger.debug(f"{self.team_id} reflected the attack back to team {attacker.team_id} at ({attacker_y}, {attacker_x})")
            grid[attacker_y, attacker_x] = self # reflect attack
            return 1  # Defense successful
        else:
            self.logger.debug(f"{self.team_id} failed to defend the attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")
            return 0  # Defense failed

    # pick_defender logic default: inherited from Class