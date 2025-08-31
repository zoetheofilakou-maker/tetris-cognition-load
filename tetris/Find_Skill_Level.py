"""
Source Video: https://www.youtube.com/watch?v=nF_crEtmpBo
"""
from main import run_game
import pygame
import sys 
import random 
import time
import os
import json
from datetime import datetime
import config
from colors import Colors
from blocks import LBlock, JBlock, IBlock, OBlock, SBlock, TBlock, ZBlock
from grid import Grid
import config

""" ------------------------------------    MAKE    YOUR    CHANGES    HERE    ------------------------"""
config.current_dificulty = "Find Skill Level"

# Time limit for the whole game
config.timer_minutes = config.find_skill_level_timer_minutes    # For Find-Skill-Level it's 6min : 2min easy, 2min medium, 2min 
config.timer_seconds = config.find_skill_level_timer_seconds

easy_starting_speed = config.easy_starting_speed
config.current_starting_speed = easy_starting_speed
config.current_speed_timer = easy_starting_speed

medium_starting_speed = config.medium_starting_speed
config.current_starting_speed = medium_starting_speed
config.current_speed_timer = medium_starting_speed

hard_starting_speed = config.hard_starting_speed
config.current_starting_speed = hard_starting_speed
config.current_speed_timer = hard_starting_speed


easy_max_speed = config.easy_max_speed
config.current_max_speed = easy_max_speed
medium_max_speed = config.medium_max_speed
config.current_max_speed = medium_max_speed
hard_max_speed = config.hard_max_speed
config.current_max_speed = hard_max_speed

# by how much the speed will increase at each increasement, in milliseconds
speed_increasement = config.speed_increasement   

# After how many line_clears do the speed increase
increase_speed_after_this_many_line_clears = config.increase_speed_after_this_many_line_clears

# After how much time will the level difficulty (speed) change
# In minutes & seconds
level_minutes = config.level_minutes
level_seconds = config.level_seconds


# to show or not show (score, line_clears, next_block or timer)
    # True = show
    # False = Don't show

show_score = config.show_score
show_line_clears = config.show_line_clears
show_next_block = config.show_next_block
show_timer = config.show_timer

# To control if the block can move after dropping the block down with down key
    # True = can't move the block after dropping down
    # False = Can move until the game updates again
lock_move = config.lock_move

"""---------------------------------------------    NO MORE CHANGES    ----------------------------------------------"""

# ---------------------------------------------    G  A  M  E    -----------------------------------------------------------------------------------------------------------------------------------------    G  A  M  E    --------
class Game:

    def __init__(self, current_speed, starting_speed, max_speed, speed_increasment,level,current_dificulty):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.current_speed = current_speed
        self.line_clears_counter = 0
        self.total_line_clears = 0
        self.game_start_time_ms = ""
        self.total_game_start_time_ms = ""
        self.level = level
        self.starting_speed = starting_speed
        self.current_max_speed = max_speed
        self.speed_increasement = speed_increasment 
        self.current_speed_timer = starting_speed
        self.current_dificulty = current_dificulty
        self.speed_pending = False      # to make sure the speed will not update during current_block, only when new block spawns
        self.all_levels_checked = False     # makes code more clearer and really makes sure that speed updates won't keep happening (can be removed with little config)
        self.show_level_change = True      # boolean to control if we should show level config for the player
        


    def write_data(self, wanted_data):
        file_name = f"{self.current_dificulty}_Data.txt"
        with open(file_name, "a+") as level_data_file:
            json.dump(wanted_data, level_data_file)
            level_data_file.write(",")
        level_data_file.close()
        print(wanted_data)


    def write_end_game_data(self, game_status):
        if self.level == "Easy":
            level_max_speed = config.easy_max_speed
        elif self.level == "Medium":
            level_max_speed = config.medium_max_speed
        elif self.level == "Hard":
            level_max_speed = config.hard_max_speed
        elif self.level == "Base":
            level_max_speed = config.easy_max_speed

        end_game_data = {
            "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
            "Game was": f"{self.current_dificulty} Level",
            "Cause of game ending": game_status,
            "Level was": self.level,
            "Time played (ms)": int(time.time() * 1000) - self.game_start_time_ms,
            "Current speed was": self.current_speed_timer,
            "Score": self.score,
            "Lines cleared": self.total_line_clears
        }
        self.write_data(end_game_data)

        
    def write_block_data(self):
        block_names = ["L Block", "J Block", "I Block", "O Block", "S Block", "T Block", "Z Block"]
        block_data = {
            "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
            "Current block": block_names[self.current_block.id - 1]
        }
        self.write_data(block_data)

    def update_score(self, lines_cleared, move_down_points):     
        global current_speed_timer

        self.total_line_clears += lines_cleared

        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared > 3:
            self.score += 700
        # adds 1 point every time a block has been placed
        self.score += move_down_points

        # for speed increasements by line_clears
        if lines_cleared != 0:
            self.line_clears_counter += 1
            if config.increase_speed_after_this_many_line_clears == 0:
                pass
            elif self.line_clears_counter == config.increase_speed_after_this_many_line_clears:
                self.line_clears_counter = 0
                cap = self.increase_speed_by_line_clears()
                if not cap:
                    speed_data = {
                        "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                        "Lines clears": lines_cleared
                    }
                    self.write_data(speed_data)
                    speed_data = {
                        "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                        "New speed": current_speed_timer
                    }
                    self.write_data(speed_data)


    def increase_speed_by_line_clears(self):
        
        if self.level == "Easy":
            level_max_speed = config.easy_max_speed
            current_max_speed = config.easy_max_speed
        elif self.level == "Medium":
            level_max_speed = config.medium_max_speed
            current_max_speed = config.medium_max_speed
        elif self.level == "Hard":
            level_max_speed = config.hard_max_speed
            current_max_speed = config.hard_max_speed
        elif self.level == "Base":
            level_max_speed = config.base_max_speed
            current_max_speed = config.base_max_speed
        elif self.level == "Find Skill Level":
            level_max_speed = config.easy_max_speed
            current_max_speed = config.hard_max_speed

        if current_max_speed == level_max_speed:
            if self.current_speed_timer - config.speed_increasement >= level_max_speed:
                pygame.time.set_timer(self.current_speed, 0)
                self.current_speed_timer -= config.speed_increasement
            else:
                speed_data = {
                    "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                    "No new speed": f"Max speed already reached, level {self.level}"
                }
                self.write_data(speed_data)
                return True

        pygame.time.set_timer(self.current_speed, self.current_speed_timer)
        return False
    


    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)
            key_data = {
                "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                "KeyDown": "Left_Key",
                "Action": "nothing"
            }
        else:
            key_data = {
                "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                "KeyDown": "Left_Key",
                "Action": "happened"
            }
        self.write_data(key_data)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)
            key_data = {
                "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                "KeyDown": "Right_Key",
                "Action": "nothing"
            }
        else:
            key_data = {
                "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                "KeyDown": "Right_Key",
                "Action": "happened"
            }
        self.write_data(key_data)

    def move_down(self):
        global block_moved_down
        self.current_block.move(1, 0)

        if not self.block_inside() or not self.block_fits():
            block_moved_down = False
            self.current_block.move(-1, 0)
            self.update_score(0, 1)
            self.lock_block()
        else:
            block_moved_down = True

    
    def hard_drop(self):
        global block_moved_down
        block_moved_down = False
    
        while self.block_inside() and self.block_fits():
            self.current_block.move(1, 0)
        
        self.current_block.move(-1, 0)  # Move back up one row since the last move was invalid
        block_moved_down = True
    
        key_data = {"Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                    "KeyDown": "HardDrop_Key",
                    "Action": "happened"}  
        self.write_data(key_data)
        self.lock_block()

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
            key_data = {
                "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                "KeyDown": "Up_Key",
                "Action": "nothing"
            }
        else:
            key_data = {
                "Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                "KeyDown": "Up_Key",
                "Action": "happened"
            }
        self.write_data(key_data)


    
    def drop_down(self):
        global block_moved_down
        block_moved_down = False
    
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
        else:
            block_moved_down = True
    
        key_data = {"Time": int(time.time() * 1000) - self.total_game_start_time_ms,
                    "KeyDown": "Down_Key",
                    "Action": "happened"}  
        self.write_data(key_data)
        if config.lock_move == True:
            self.lock_block()
        
    # switch from current block to new blcok
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id

        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        

        if self.block_fits() == False:
            self.current_block = "Nothing"  # controls whether current block will be drawn if it doesn't fit the grid
            self.game_over = True
        else:
            self.write_block_data()

        self.update_speed_and_level()

    def update_speed_and_level(self):
        global current_max_speed, easy_max_speed, medium_max_speed, hard_max_speed
        global current_speed, current_speed_timer
        global change_level, change_level_timer
        global level_notice_timer
        global start_level_notice_timer

        if self.all_levels_checked == False:
            if self.speed_pending == True:
                self.speed_pending = False

                pygame.time.set_timer(change_level, 0)  # reset/stop timer

                if current_max_speed == config.medium_max_speed:  # update to hard level
                    current_max_speed = hard_max_speed
                    level_data = {"Time": int(time.time() * 1000) - game.game_start_time_ms,
                                "Entering level": "Hard"}
                    self.write_data(level_data)

                    self.show_level_change = True
                    level_notice_timer = 5
                    start_level_notice_timer = time.time()

                    current_speed_timer = hard_starting_speed
                    pygame.time.set_timer(current_speed, current_speed_timer)
                    speed_data = {"Time": int(time.time() * 1000) - game.game_start_time_ms,
                                "New speed": current_speed_timer}
                    self.write_data(speed_data)
                    self.all_levels_checked = True

                if current_max_speed == easy_max_speed:  # update to medium level
                    current_max_speed = medium_max_speed
                    level_data = {"Time": int(time.time() * 1000) - game.game_start_time_ms,
                                "Entering level": "Medium"}
                    self.write_data(level_data)

                    self.show_level_change = True
                    level_notice_timer = 5
                    start_level_notice_timer = time.time()

                    current_speed_timer = medium_starting_speed
                    pygame.time.set_timer(current_speed, current_speed_timer)
                    speed_data = {"Time": int(time.time() * 1000) - game.game_start_time_ms,
                                "New speed": current_speed_timer}
                    self.write_data(speed_data)

                pygame.time.set_timer(change_level, change_level_timer)


    # waiting screen / start_screen is displayed only at the beginning of the whole code before real game starts
    # player can continue to the game by pressing any key (change later to only allow arrowKey inputs)
    def waiting_screen(self):
        global level_notice_timer, start_level_notice_timer
        global screen
        global scale_x, scale_y
        global scale_w, scale_h

        waiting = True
        while waiting:

            screen.fill(Colors.dark_blue) # whole screen

            start_surface1 = config.title_font.render(f"-- {self.current_dificulty}  --", True, Colors.orange)
            start_surface1_rect = start_surface1.get_rect(center=(screen.get_width() // 2, 80))
            screen.blit(start_surface1, start_surface1_rect)

            start_surface2 = config.title_font.render("To start", True, Colors.yellow)
            start_surface2_rect = start_surface2.get_rect(center=(screen.get_width() // 2, 150))
            screen.blit(start_surface2, start_surface2_rect)

            start_surface3 = config.title_font.render("press any of your arrow keys", True, Colors.yellow)
            start_surface3_rect = start_surface3.get_rect(center=(screen.get_width() // 2, 190))
            screen.blit(start_surface3, start_surface3_rect)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    game_start_date = datetime.now().strftime("%A %d/%m/%Y %H:%M:%S:%f")
                    self.total_game_start_time_ms = int(time.time() * 1000)
                    self.game_start_time_ms = int(time.time() * 1000)
                    self.level_change_time = time.time() # Initialize the level change timer
                    start_level_notice_timer = time.time()
                    level_notice_timer = 5

                    if self.level == "Easy":
                        level_max_speed = config.easy_max_speed
                    elif self.level == "Medium":
                        level_max_speed = config.medium_max_speed
                    elif self.level == "Hard":
                        level_max_speed = config.hard_max_speed
                    elif self.level == "Base":
                        level_max_speed = config.base_max_speed
                    elif self.level == "Find Skill Level":
                        level_max_speed = config.hard_max_speed

                    if config.current_dificulty == "Find Skill Level":
                        game_start_data = {"Game started": game_start_date,
                                           "Game": "Find Skill Level",
                                           "Start level": self.level,
                                           "Starting speed": current_speed_timer,
                                            "Selected settings": {
                                            "Time Limit": str(config.find_skill_level_timer_minutes)+ " min " + str(config.find_skill_level_timer_seconds) + " s",
                                            "Starting level speeds": {"Easy start speed": config.easy_starting_speed,
                                            "Medium start speed": config.medium_starting_speed,
                                            "Hard start speed": config.hard_starting_speed},
                                            "Maximum level speeds": {"Easy max speed": easy_max_speed,
                                            "Medium max speed": medium_max_speed,
                                            "Hard max speed": hard_max_speed},
                                            "Speed increases by": config.speed_increasement},
                                            "Increase speed after this many line clears": config.increase_speed_after_this_many_line_clears,
                                            "Change level after": str(config.level_minutes) + " min " + str(config.level_seconds) + " s",
                                            "Show score": config.show_score,
                                            "Show line clears":config. show_line_clears,
                                            "Show next block": config.show_next_block,
                                            "Show timer": config.show_timer,
                                            "Lock block movement":config.lock_move}
                    else:
                        game_start_data = {
                            "Game started": game_start_date,
                            "Game": f"{self.level} Level",
                            "Start level": self.level,
                            "Starting speed": config.current_speed_timer,
                            "Selected settings": {
                                "Time Limit": f"{config.timer_minutes} min {config.timer_seconds} s",
                                "Starting level speeds": {f"{self.level} start speed": config.current_speed_timer},
                                "Maximum level speeds": {f"{self.level} max speed": level_max_speed},
                                "Speed increases by": config.speed_increasement
                            },
                            "Increase speed after this many line clears": config.increase_speed_after_this_many_line_clears,
                            "Show score": config.show_score,
                            "Show line clears":config.show_line_clears,
                            "Show next block": config.show_next_block,
                            "Show timer": config.show_timer,
                            "Lock block movement": config.lock_move
                        }

                    self.write_data(game_start_data)
                    self.write_block_data()
                    waiting = False

                    if event.type == pygame.QUIT:
                        game_data = {"Cause of game ending": "Pressed quit at the start screen"}
                        self.write_data(game_data)
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.VIDEORESIZE:
                        screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        scale_w = 500 + ((event.h - 620.0)) - 3
                        scale_h = 620 + ((event.h - 620.0)) - 3
                        scale_x = (event.w - scale_w) / 2.0
                        scale_y = 1.0

            pygame.display.update()

    def game_over_screen(self):
        pygame.draw.rect(screen, Colors.dark_blue, pygame.Rect(40, 190, 250, 120))
        game_over_surface1 = config.title_font.render("Game Over.", True, Colors.red)
        game_over_surface2 = config.game_over_font.render("Press any arrow,", True, Colors.yellow)
        game_over_surface3 = config.game_over_font.render("to continue.", True, Colors.yellow)
        screen.blit(game_over_surface1, (90, 200))
        screen.blit(game_over_surface2, (90, 260))
        screen.blit(game_over_surface3, (90, 280))
        pygame.display.update()


    # when timer is at 0 (aka. time has ended)
    def time_over_screen(self):
        #end_time = time.time() - start_time
        game_status = "Time ended"
        self.write_end_game_data(game_status)

        game.game_over == False

        end_time_limit = 3 # show endscreen for 3 seconds
        end_screen_start_time = time.time()     # to start the timer
        show_end_timer = True

        while show_end_timer:
            pygame.draw.rect(screen, Colors.soft_blue, pygame.Rect(100, 260, 320, 40))         # change colors
            time_over_surface = config.time_ended_font.render("Time has ended.", True, Colors.dark_grey)
            screen.blit(time_over_surface, (110, 260))
            pygame.display.update()

            end_screen_elapsed_time = time.time() - end_screen_start_time

            for event in pygame.event.get():
                if end_screen_elapsed_time > end_time_limit:
                    show_end_timer = False
                if event.type == pygame.QUIT:
                    game_data = {"Cause of game ending": "Pressed quit at the time over screen"}
                    self.write_data(game_data)
                    pygame.quit()
                    sys.exit()
        pygame.quit()
        sys.exit()

    # whenever ever the player loses
    def true_game_over_screen(self):

        true_end_time_limit = 3     # show true game over screen for 3 seconds
        true_end_screen_start_time = time.time()    # to start the timer
        true_end_timer = True

        while true_end_timer:
            true_end_screen_elapsed_time = time.time() - true_end_screen_start_time
            
            pygame.draw.rect(screen, Colors.soft_blue, pygame.Rect(30, 250, 400, 100))         # change colors
            time_over_surface = config.time_ended_font.render("Game Over.", True, Colors.red)
            time_over_surface2 = config.guide_font.render("We have found your skill level.", True, Colors.dark_blue)
            screen.blit(time_over_surface, (110, 260))
            screen.blit(time_over_surface2, (40, 310))
            pygame.display.update()

            if true_end_screen_elapsed_time > true_end_time_limit:
                true_end_timer = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_data = {"Cause of game ending": "Pressed quit at the game over screen"}
                    game.write_data(game_data)
                    pygame.quit()
                    sys.exit()
        
        pygame.quit()
        sys.exit()

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.total_line_clears = 0
        if not config.current_dificulty == "Find Skill Level":
            self.game_start_time_ms = int(time.time() * 1000)

    # checks if the tiles of the current block overlap with the already placed blocks
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True


    # checks if any tiles of current block is outside the grid
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True
    
    # draws blocks on the screen (last code when drawing on the game)
    def draw(self, screen):
        self.grid.draw(screen)
        if self.current_block != "Nothing":     # doesn't draw the block if it doesn't fit
            self.current_block.draw(screen, 11, 11) # draws the current block

        # defines the positions where to draw the next block info
        # to control how big the next blocks are go to Class Block --> def draw_next_block
        if show_next_block == True:
            if self.next_block.id == 3:     # I Block
                self.next_block.draw(screen, 255, 350)
            elif self.next_block.id == 4:   # O Block
                self.next_block.draw(screen, 255, 340)
            else:
                self.next_block.draw(screen, 270, 330)


        if self.show_level_change == True:
            # Easy - Level
            if current_max_speed == config.easy_max_speed:
                notice_text = config.title_font.render("Level - Easy", True, Colors.white)
                screen.blit(notice_text, (80, 110))
                self.level = "Easy"

                if (time.time() - start_level_notice_timer) >= level_notice_timer:
                    self.show_level_change = False

            # Medium - Level
            if current_max_speed == config.medium_max_speed:
                notice_text = config.title_font.render("Level - Medium", True, Colors.white)
                screen.blit(notice_text, (60, 110))
                self.level = "Medium"

                if (time.time() - start_level_notice_timer) >= level_notice_timer:
                    self.show_level_change = False

            # Hard - Level
            if current_max_speed == config.hard_max_speed:
                notice_text = config.title_font.render("Level - Hard", True, Colors.white)
                screen.blit(notice_text, (80, 110))
                self.level = "Hard"

                if (time.time() - start_level_notice_timer) >= level_notice_timer:
                    self.show_level_change = False

    def draw_during_run(self,elapsed_time):
        screen.fill(Colors.dark_blue)

        if config.show_score:
            score_rect = pygame.Rect(320, 55, 170, 60)
            pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
            score_surface = config.title_font.render("Score", True, Colors.white)
            screen.blit(score_surface, (365, 20))
            score_value_surface = config.title_font.render(str(self.score), True, Colors.white)
            screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))

        if config.show_line_clears:
            line_clears_rect = pygame.Rect(320, 175, 170, 60)
            pygame.draw.rect(screen, Colors.light_blue, line_clears_rect, 0, 10)
            line_clears_surface = config.guide_font.render("Lines Cleared", True, Colors.white)
            screen.blit(line_clears_surface, (330, 140))
            lines_cleared_nums = config.title_font.render(str(self.total_line_clears), True, Colors.white)
            screen.blit(lines_cleared_nums, (397, 190))

        if config.show_next_block:
            next_rect = pygame.Rect(320, 290, 170, 160)
            pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
            next_surface = config.title_font.render("Next", True, Colors.white)
            screen.blit(next_surface, (375, 255))

        if config.show_timer:
            player_timer_rect = pygame.Rect(320, 500, 170, 90)
            pygame.draw.rect(screen, Colors.light_blue, player_timer_rect, 0, 10)
            if self.current_dificulty == "Base":
                player_timer_surface = config.title_font.render(str((config.base_time_limit - int(elapsed_time))), True, Colors.white)
            elif self.current_dificulty == "Find Skill Level":
                player_timer_surface = config.title_font.render(str((config.find_skill_level_time_limit - int(elapsed_time))), True, Colors.white)
            else:
                player_timer_surface = config.title_font.render(str((config.time_limit - int(elapsed_time))), True, Colors.white)
            screen.blit(player_timer_surface, player_timer_surface.get_rect(centerx=player_timer_rect.centerx, centery=player_timer_rect.centery))
            player_timer = config.title_font.render("Timer", True, Colors.white)
            screen.blit(player_timer, (365, 465))

        #self.update_level_based_on_time(elapsed_time)
        self.draw(screen)
        pygame.display.update()

# -------------------------------------    M  A  I  N    ----------------------------------------------------------------------------------------------------------------------------------------------------    M  A  I  N    ----------


"""
Game Loop

1. Event Handling
2. Updating Positions
3. Drawing Objects 

"""

os.environ["SDL_VIDEO_CENTERED"] = "1"      # tries to center your window the best it can
pygame.init()

info = pygame.display.Info()       # to get computer width/height
screen_width, screen_height = info.current_w, info.current_h

screen = pygame.display.set_mode((500, 620), pygame.RESIZABLE)
scale_x = 1.0
scale_y = 1.0

scale_w = 500 - 3
scale_h = 620 - 3

pygame.display.set_caption("Python Tetris - "+config.current_dificulty) # give title



# -------------------------------------------- E V E N T S ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    E V E N T S    -----------------
clock = pygame.time.Clock() # fps
current_speed = pygame.USEREVENT
current_speed_timer = config.current_starting_speed  # in milliseconds
pygame.time.set_timer(current_speed, current_speed_timer)

game = Game(current_speed, config.current_starting_speed, config.current_max_speed, config.speed_increasement, config.current_dificulty,config.current_dificulty)

# Falling speed of the blocks           # will keep changing at all levels, starting speed is from level Easy
current_speed = pygame.USEREVENT
current_speed_timer = config.easy_starting_speed       # in milliseconds
pygame.time.set_timer(current_speed, current_speed_timer)


# Next level in milliseconds            # After set amount of time, change level and allow the speed to increase to the new level's max_speed
change_level = pygame.USEREVENT + 1
change_level_timer = (config.level_minutes * 60 * 1000) + (config.level_seconds * 1000)       # in milliseconds
pygame.time.set_timer(change_level, change_level_timer)

time_limit = (config.find_skill_level_timer_minutes * 60 + config.find_skill_level_timer_seconds) # in seconds

current_max_speed = config.easy_max_speed        # Has to be same as easy_max_speed at start

start_screen = True
block_moved_down = False    # To fix bugs where block would fall immediately when player would exit different screen with down.key (if current block has been moved by game update)

#---------------------------------------    G A M E    R U N N I N G    ------------------------------------------------------------------------------------------------------------------------------------------------------------    G A M E    R U N N I N G    -------------"""
while True:
    for event in pygame.event.get():

        #starting screen
        if start_screen:                # start_screen = True first, then it will stay false, so will only run once
            game.waiting_screen()
            start_screen = False
            start_time = time.time()    # start timer, right after the starting screen has gone away, after pressing any key
            game.show_level_change = True   # Shows player that they start at the level easy
        
        
        elapsed_time = time.time() - start_time

        # time has ended
        if elapsed_time >= time_limit:
            game.time_over_screen()

        # to leave the game
        if  event.type == pygame.QUIT:
            game_data = {"Cause of game ending": "Pressed quit during game play"}
            game.write_data(game_data)
            game_status = "Quit"
            game.write_end_game_data(game_status)
            pygame.quit()
            sys.exit()
  
        # True Game Over                # if player loses even once, the whole game will end
        if game.game_over == True:
                end_time = start_time - time.time()
                game_status = "Game Over"
                game.write_end_game_data(game_status)
                game.true_game_over_screen()         
            
        # keyboard events     
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()

            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()

            if event.key == pygame.K_SPACE and game.game_over == False:
                game.hard_drop()

            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()

        # Block falling speed
        if event.type == current_speed and game.game_over == False:
            game.move_down()

        # Level update after set amount of time
        if event.type == change_level:
            game.speed_pending = True
            

    game.draw_during_run(elapsed_time)  #drawing
    clock.tick(60)  # while loop and all the code inside of it will run 60 times per second
