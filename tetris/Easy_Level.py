"""
Source Video: https://www.youtube.com/watch?v=nF_crEtmpBo
"""

import config
from main import run_game

def main(main_menu):
    config.current_dificulty = "Easy"

    config.timer_minutes = config.level_timer_minutes
    config.timer_seconds = config.level_timer_seconds

    easy_starting_speed = config.easy_starting_speed
    config.current_starting_speed = easy_starting_speed
    config.current_speed_timer = easy_starting_speed

    # To check that speed doesn't increase faster that the current level allows
    # In milliseconds
    easy_max_speed = config.easy_max_speed
    config.current_max_speed = easy_max_speed

    # by how much the speed will increase at each increasement, in milliseconds
    speed_increasement = config.speed_increasement

    # After how many line_clears do the speed increase
    increase_speed_after_this_many_line_clears = config.increase_speed_after_this_many_line_clears
    
    run_game(main_menu)

if __name__ == "__main__":
    main()
