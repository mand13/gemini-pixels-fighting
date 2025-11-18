# gemini-pixels-fighting
This is a pixels fighting game that I created using almost exclusively Gemini code generation (up until the version where I added classes, most of the work was written by hand after that). I've prompted it to add many features including some percent control statistics and plots of team control over time.

## Character Classes

### Sniper
    <explanation>
    ...

### Snowball (not yet implemented):
    When snowball is the chosen attacker, it selects the entire contiguous group of snowballs, and moves it in a random direction, overtaking any pixels that are in the way, and still leaving behind it's members that were already there.

### IDEAS:
- Class Ideas: Paint bucket/super plague, rook, bomber, snowball
    - Add some sort of troop that, when attacked, may relay that attack to some third party who wasn't involved (call it the instigator?)
    - make it so zombies can win the game (even display a percentage of zombies perhaps on the scoreboard) (they have default mechanics, but the necromancer can revive them to be on their team when they interact together) (maybe there is always a zombie team that just doesn't get assigned any pixels at the start)
    - implement display for healer's hp
    - Currently too weak (I think): Nomad, sniper, assassin
    - Currently too strong (I think): Berserker, necromancer

- collect data and do analysis to determine OP teams and influence balance changes
- implement team win for whoever has most pixels in the event of a standstill
- Add command-line argument to play default style game
- Add more in-depth explanation of the game to README (including all classes and what they do, why/how I made the game, etc)
- Maybe add saving feature so I can save the status of a currently running game to come back to later. This would be like a more advanced version of the pause feature.






