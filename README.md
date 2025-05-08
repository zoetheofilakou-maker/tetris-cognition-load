# Game Structure: 

 1. Base Level - Familiarity:

    - Explain the controls and rules of the game to partisipant.
    - Slowest level.
    - No speed increasements.
    - After partisipant has learned the controls and rules, proseed to next phase of the test.

2. Find Skill Level:

    - Play on Base level.
    - 3 min.
    - Tell the partisipant to try clear as many lines they can in the time limit.
    - Number of line clears determen the assigned skill level.
    - Less than 10 -> Easy.
    - 10 to 20 -> Medium.
    - 20 or more -> Hard.
    - IMPORTANT: Stydy guide must tell the player what level they are assigned to.

3. Mental workload:

    - if player assigned level --easy-- or --medium-- (during Find-Skill-Level) -->
            - Easy 10 min.
                - Fill first survey.
            - Medium 10 min.
                - Fill second survey.

    - if player assigned level --hard-- (during Find-Skill-Level) -->
            - Medium 10 min.
                - Fill first survey.
            - Hard 10 min.
                - Fill second survey.



# Data Structure:
Log file is created for every level when playing any level named "*level_name*_data.txt" E.g: Hard_Level_Data.txt.
New file is created if none exist before, or if file exist, it is appended.

    separeted with ; 

    example. {"game_data": "some value"};{"end_data": {"Level": "easy"}, {"speed": "speed value"}}

# Collected data: 

various a bit depending on the game

## Quit data

            - game was interrupted, stopped and quitted because someone pressed quit key
                (will tell when it was pressed: during start screen, during gaming, during game over screen, during time over)
                (will also give game_end_data)

## When game starts

            - precise time & day
            - what game (Base Level, Find Skill Level, Easy, Medium or Hard)
            - starting speed
            - selected settings
                    - time limit for the whole game/code
                    - starting speeds for levels
                            - easy
                            - medium
                            - hard
                    -maximum speeds for levels
                            - easy
                            - medium
                            - hard
                    - speed increasement
                    - increase speed after this many line clears
                    - times after which the level difficulty changes
                    - show score
                    - show line clears
                    - show next block
                    - show timer
                    - lock block movement
    
    
## While playing

            - block data
                    - timestamp
                    - current block (aka. what block is currently after previous block was put down)


            - key press data
                    - timestamp
                    - what key pressed (down key is an exeption, since that will always )
                    - action
                            - happened (if something happened when that key was pressed)
                            - nothing (if pressing the key didn't affect the game at all)


            - speed increase data
                    - timestamp
                    - speed increased by
                            - line clears
                                    - new speed
                            - level change
                                    - what new level
                                    - new speed
                            - nothing
                                    - maximum speed of the level has already achieved (when line clears don't increase speed anymore)


# When game ends

            - timestamp
            - what game was
            - reason why game ended (game over, time over)
            - what most recent level was
            - how much game played during that game
            - what most recent speed was
            - score
            - lines cleared

## The log looks something like this:

{"Game started": "Friday 18/10/2024 10:05:51:697365", "Game": "Hard Level", "Start level": "Hard", "Starting speed": 200, "Selected settings": {"Time Limit": "10 min 0 s", "Starting level speeds": {"Hard start speed": 200}, "Maximum level speeds": {"Hard max speed": 200}, "Speed increases by": 20}, "Increase speed after this many line clears": 1, "Show score": true, "Show line clears": true, "Show next block": true, "Show timer": true, "Lock block movement": false},{"Time": 50, "Current block": "I Block"},{"Time": 695, "KeyDown": "Up_Key", "Action": "happened"},{"Time": 888, "KeyDown": "Left_Key", "Action": "happened"},{"Time": 1065, "KeyDown": "Left_Key", "Action": "happened"},{"Time": 1248, "KeyDown": "Left_Key", "Action": "happened"},{"Time": 1586, "KeyDown": "Left_Key", "Action": "happened"},{"Time": 1781, "KeyDown": "Left_Key", "Action": "happened"},{"Time": 2024, "KeyDown": "Left_Key", "Action": "nothing"},{"Time": 181919, "KeyDown": "HardDrop_Key", "Action": "happened"},{"Time": 181955, "Game was": "Hard Level", "Cause of game ending": "Game Over", "Level was": "Hard", "Time played (ms)": 100173, "Current speed was": 200, "Score": 1713, "Lines cleared": 14},{"Time": 182401, "Game reset": "Game started again after game over"},{"Time": 182437, "Current block": "Z Block"},{"Cause of game ending": "Pressed escape during game play"},{"Time": 183221, "Game was": "Hard Level", "Cause of game ending": "Quit", "Level was": "Hard", "Time played (ms)": 784, "Current speed was": 200, "Score": 0, "Lines cleared": 0},