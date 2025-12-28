# nomad.py
"""
This module defines the Nomad class, a subclass of Class

The Nomad swaps places with pixels from some distance away before attackin an adjacent pixel and they are immune to defense.

TODO improve description
"""

import random
import logging
from . import Class

class Nomad(Class):
    def __init__(self, team_id, color, level=logging.INFO):
        super().__init__(team_id, color, level=level)
        self.swap_range = 7 # distance to swap before attacking

    def attack(self, grid, attacker_y, attacker_x):
        """
        nomad attack logic TODO improve description
        """
        # swap with a random pixel within swap_range
        dy = random.choice([-self.swap_range, 0, self.swap_range])
        dx = random.choice([-self.swap_range, 0, self.swap_range])
        swap_y = (attacker_y + dy) % grid.shape[0]
        swap_x = (attacker_x + dx) % grid.shape[1]
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} swaps with team {grid[swap_y, swap_x].team_id} from ({attacker_y}, {attacker_x}) to ({swap_y}, {swap_x})")
        grid[attacker_y, attacker_x], grid[swap_y, swap_x] = grid[swap_y, swap_x], grid[attacker_y, attacker_x]

        # now pick a defender adjacent to the new position to attack
        defender_y, defender_x = self.pick_defender(grid, swap_y, swap_x)
        defender = grid[defender_y, defender_x]
        self.logger.debug(f"{self.__class__.__name__} from team {self.team_id} captures from ({swap_y}, {swap_x}) to team {defender.team_id} at ({defender_y}, {defender_x})")
        # the nomad is immune to defense, so it always captures the pixel
        grid[defender_y, defender_x] = self
        return 1 # Attack successful

    # defend logic default: inherited from Class

    # pick_defender logic default: inherited from Class