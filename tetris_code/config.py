import pygame

pygame.font.init()
""" ------------------------------------    MAKE    YOUR    CHANGES    HERE    ------------------------"""

# Variable for game time initialization
timer_minutes = 10 
timer_seconds = 0

# Time limit for easy, medium and hard levels
# Change the time limit here
level_timer_minutes = 10
level_timer_seconds = 0


# Time limit for the base game
# Change the time limit here
base_timer_minutes = 3
base_timer_seconds = 0

# Time limit for the Find-Skill-Level game
# These are not in use at the moment
find_skill_level_timer_minutes = 6
find_skill_level_timer_seconds = 0


# After how much time will the level difficulty (speed) change in find_skill_level
# These are not in use at the moment
level_minutes = 2 
level_seconds = 0 


time_limit = (timer_minutes * 60 + timer_seconds) # in seconds
base_time_limit = (base_timer_minutes * 60 + base_timer_seconds) # in seconds
find_skill_level_time_limit = (find_skill_level_timer_minutes * 60 + find_skill_level_timer_seconds) # in seconds

# Speeds to increase to when level changes aka. starting speeds at each level
# The smaller number, the faster game updates the speed (aka. faster game)
base_starting_speed = 600
easy_starting_speed = 600
medium_starting_speed = 400
hard_starting_speed = 300
current_speed_timer = 600

current_starting_speed = 200


# To check that speed doesn't increase faster that the current level allows

# Smaller number = faster max speed
base_max_speed = base_starting_speed
easy_max_speed = 400 # Default 400
medium_max_speed = 300 # Default 300
hard_max_speed = 200   # Default 200     # to make sure the speed doesn't exceed certain point, cause otherwis

current_max_speed = 200
# by how much the speed will increase at each increasement, in milliseconds
speed_increasement = 20  

# After how many line_clears do the speed increase
increase_speed_after_this_many_line_clears = 1


current_dificulty = "default"


# to show or not show (score, line_clears, next_block or timer)
    # True = show
    # False = Don't show

show_score = True
show_line_clears = True
show_next_block = True
show_timer = True

# To control if the block can move after dropping the block down with down key
    # True = can't move the block after dropping down
    # False = Can move until the game updates again
lock_move = False

# Font sizes for the game
title_font = pygame.font.Font(None, 40)
arrow_font = pygame.font.Font(None, 70)
guide_font = pygame.font.Font(None, 35)
game_over_font = pygame.font.Font(None, 25)
time_ended_font = pygame.font.Font(None, 55)

"""---------------------------------------------    NO MORE CHANGES    ----------------------------------------------"""
