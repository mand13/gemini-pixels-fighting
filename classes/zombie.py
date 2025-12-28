# zombie.py
"""
This module defines the Zombie class, a subclass of Class

TODO improve description
"""

import random
import logging
from . import Class

class Zombie(Class): # TODO actually implement this class
    def __init__(self, team_id, color, level=logging.INFO):
        super().__init__(team_id, color, level=level)

    # attack logic default: inherited from Class

    # defend logic default: inherited from Class

    # pick_defender logic default: inherited from Class