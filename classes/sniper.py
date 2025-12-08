# sniper.py
"""
This module defines the Sniper class, a subclass of Class, which implements specific attack and defend mechanics for the Sniper team in the game.

The Sniper has an attack range of 10 pixels and a 40% chance to successfully defend against any attack.
"""

import random
import logging
from . import Class

class Sniper(Class):
    def __init__(self, team_id, level=logging.INFO):
        super().__init__(team_id, level)
        self.range = 10

    # attack logic default: inherited from Class

    def defend(self, grid, defender_y, defender_x, attacker, attacker_y, attacker_x):
        """
        Sniper-specific defend logic

        The Sniper is sneaky, and thus has a 40% chance to successfully defend against any attack.
        """
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} defends at ({defender_y}, {defender_x}) against attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")

        if random.random() < 0.4:
            self.logger.debug(f"{self.team_id} successfully defended ({defender_y}, {defender_x}) against an attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")
            return 1 # Defense successful
        else:
            self.logger.debug(f"{self.team_id} failed to defend ({defender_y}, {defender_x}) against an attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")
            return 0 # Defense failed
    
    # pick_defender logic default: inherited from Class (but self.range is increased)