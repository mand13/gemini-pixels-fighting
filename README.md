# gemini-pixels-fighting
This is a pixels fighting game that I created using almost exclusively Gemini code generation. I've prompted it to add many features including some percent control statistics and plots of team control over time.

TODO:
monte-carlo.py hasn't been updated. It could be updated to track many extra stats that would be interesting to analyze like each team's min and max percents (maybe all percents if not too expensive?)

Maybe add saving feature so I can save the status of a currently running game to come back to later. This would be like a more advanced version of the pause feature.

I should add classes. Each class would have different mechanics. Maybe there could be a very strong defensive class, a strong offensive class, a class with default mechanics, etc.
    - An idea is to add one where a pixel can attack any pixel on the board and basically copy/paste a giant contiguous collection of pixels of that color to somewhere, but with somewhat low probability.
    - a healer who, if they attack themself, actually just adds a "hitpoint"

Current list of classes and what they do:
["Berserker", "Sniper", "Assassin", "Bunker", "Phalanx", "Thorns", "Plague", "Nomad", "Necromancer", "Healer"]

Currently too weak: Nomad, sniper, assassin
Too strong: Berserker, necromancer

Add argument to play default style game

implement display for healer's hp

implement team win for whoever has most pixels in the event of a standstill

collect data to analyze which teams are OP

Make sniper sneaky

Class Ideas: Paint bucket/super plague, mortar, rook, bomber, 

make it so zombies can win the game (even display a percentage of zombies perhaps on the scoreboard) (they attack like normal, but the necromancer can revive them to be on their team)



