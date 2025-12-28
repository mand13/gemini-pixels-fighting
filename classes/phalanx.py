# phalanx.py
"""
This module defines the Phalanx class, a subclass of Class

TODO improve description
"""

import random
import logging
from . import Class

class Phalanx(Class):
    def __init__(self, team_id, level=logging.INFO):
        super().__init__(team_id, level=level)

    # attack logic default: inherited from Class

    def defend(self, grid, defender_y, defender_x, attacker, attacker_y, attacker_x):
        """
        Phalanx-specific defend logic TODO improve description
        """
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} defends at ({defender_y}, {defender_x}) against attack from team {attacker.team_id} at ({attacker_y}, {attacker_x})")

        # Implement defend mechanics here
        # count adjacent allies
        ally_count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny = (defender_y + dy) % grid.shape[0]
                nx = (defender_x + dx) % grid.shape[1]
                if grid[ny, nx] == self.team_id:
                    ally_count += 1
        if ally_count >= 4:
            return 1 # Phalanx defended successfully
        else:
            return 0 # Defense failed

    # pick_defender logic default: inherited from Class