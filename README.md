# gemini-pixels-fighting
This is a pixels fighting game that I created using almost exclusively Gemini code generation (up until the version where I added classes, most of the work was written by hand after that). I've prompted it to add many features including some percent control statistics and plots of team control over time.


## Character Classes

### Sniper
    <explanation>
    ...

### Snowball (not yet implemented):
    When snowball is the chosen attacker, it selects the entire contiguous group of snowballs, and moves it in a random direction, overtaking any pixels that are in the way, and still leaving behind it's members that were already there.


## IDEAS:
- Class Ideas: Paint bucket/super plague, rook, bomber, snowball, swapper, bishop
    - Add some sort of troop that, when attacked, may relay that attack to some third party who wasn't involved (call it the instigator?)
    - NECROMANCER REWORK: make it so zombies can win the game (even display a percentage of zombies perhaps on the scoreboard) (they have default mechanics, but the necromancer can revive them to be on their team when they interact together) (maybe there is always a zombie team that just doesn't get assigned any pixels at the start)
    - implement display for healer's hp
    - Currently too weak (I think): Nomad, sniper, assassin
    - Currently too strong (I think): Berserker, necromancer, Healer
    - come up with ways to prevent the common causes of dynamic stand-still, or ways to declare a victor/tie in this scenario
        - mortar v mortar
        - berserker v berserker
        - mortar v berserker
        - plague v mortar
        - phalanx v anything not ranged (static stand-still)
        - necromancer v mortar

- collect data and do analysis to determine OP teams and influence balance changes
- implement team win for whoever has most pixels in the event of a standstill
- Add command-line argument to play default style game
- Add more in-depth explanation of the game to README (including all classes and what they do, why/how I made the game, etc)
- Maybe add saving feature so I can save the status of a currently running game to come back to later. This would be like a more advanced version of the pause feature.
- Add feature to save game progress even if it doesn't end and I quit premature
- Widen sidebar
- add feature to customize which classes are playing
- I really want there to be a reason for fires to start and spread and do something neat (this may be what prevents dynamic/static stand-stills)
- add game speed-up and slow down feature
- implement object-oriented approach for classes to simplify code and updates, etc
- write a script that automatically executes every 1v1 game


## Notes about class dynamics
- Necromancer easily defeats literally everything except mortar, which results in a standstill probably?
- Healer easily defeats literally everything except necromancer which dominates it instantly
- Mortar and Berserker are very evenly matched but dominate everything except necromancer and healer (for the most part) sometimes thorns and plague do well

### 1v1 Results
- Assassin beats Plague
- Healer beats Berserker
- Plague beats Nomad





