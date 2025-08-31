import sys

import json
import time
import random
import pygame
from datetime import datetime
from blocks import IBlock, JBlock, LBlock, OBlock, SBlock, TBlock, ZBlock
from grid import Grid
from colors import Colors
import config
import api
from api import sendudp, sendtcp
from utils import return_to_main_menu
from api import send_score_update, send_level_update, send_line_clear_summary, send_scene_end


screen = pygame.display.set_mode((500, 620), pygame.RESIZABLE)

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
        self.total_game_start_time_ms = ""
        self.game_start_time_ms = ""
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
        """ if self.level == "Easy":
            level_max_speed = config.easy_max_speed
        elif self.level == "Medium":
            level_max_speed = config.medium_max_speed
        elif self.level == "Hard":
            level_max_speed = config.hard_max_speed
        elif self.level == "Base":
            level_max_speed = config.easy_max_speed
 """
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

        #send final lineclear summary to iMotions
        send_score_update(self.score)
        send_level_update(self.level)
        send_line_clear_summary(self.total_line_clears)
        send_scene_end(self.current_dificulty + "Level")

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
        self.score += move_down_points

        print(f"Score updated:{self.score}")
        send_score_update(self.score)

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
                        "New speed": self.current_speed_timer
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
            level_max_speed = config.hard_max_speed
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

    # Drop the block down to the bottom
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


    # drop the block down one row
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

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id

        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)

        if not self.block_fits():
            self.current_block = "Nothing"
            self.game_over = True

        # End the current gameplay scene and send GameOver marker
            api.send_scene_end(self.level + "Level")
            api.send_event_marker("GameOver", "Player finished the game")
            sys.stdout.flush()
            time.sleep(0.001)
        else:
            self.write_block_data()

        self.update_speed_and_level()

    # Legacy game function
    def update_speed_and_level(self):
        global current_max_speed, easy_max_speed, medium_max_speed, hard_max_speed
        global current_speed, current_speed_timer
        global change_level, change_level_timer
        global level_notice_timer
        global start_level_notice_timer

        previous_level =self.level #store current level

        if self.all_levels_checked == False:
            if self.speed_pending == True:
                self.speed_pending = False

                pygame.time.set_timer(change_level, 0)  # reset/stop timer

                if current_max_speed == config.medium_max_speed:  # update to hard level
                    current_max_speed = config.hard_max_speed
                    level_data = {"Time": int(time.time() * 1000) - self.game_start_time_ms,
                                "Entering level": "Hard"}
                    self.write_data(level_data)

                    self.show_level_change = True
                    level_notice_timer = 5
                    start_level_notice_timer = time.time()

                    current_speed_timer = config.hard_starting_speed
                    pygame.time.set_timer(self.current_speed, current_speed_timer)
                    speed_data = {"Time": int(time.time() * 1000) - self.game_start_time_ms,
                                "New speed": current_speed_timer}
                    self.write_data(speed_data)
                    self.all_levels_checked = True

                if current_max_speed == config.easy_max_speed:  # update to medium level
                    current_max_speed = config.medium_max_speed
                    level_data = {"Time": int(time.time() * 1000) - self.game_start_time_ms,
                                "Entering level": "Medium"}
                    self.write_data(level_data)

                    self.show_level_change = True
                    level_notice_timer = 5
                    start_level_notice_timer = time.time()

                    current_speed_timer = config.medium_starting_speed
                    pygame.time.set_timer(self.current_speed, current_speed_timer)
                    speed_data = {"Time": int(time.time() * 1000) - self.game_start_time_ms,
                                "New speed": current_speed_timer}
                    self.write_data(speed_data)

                if self.level != previous_level:
                    print(f"Level Update:{self.level}")
                    send_level_update(self.level)

                pygame.time.set_timer(change_level, change_level_timer)

    def waiting_screen(self):
        global start_level_notice_timer, level_notice_timer
        global screen
        global scale_x, scale_y
        global scale_w, scale_h

        waiting = True
        while waiting:
            screen.fill(Colors.dark_blue)


            # Combine the message into a single string with newline characters
            message = f"\n \n-- {self.current_dificulty}  --\nTo start\npress any of your arrow keys"
            lines = message.split('\n')

            font = config.title_font
            line_height = font.get_linesize()
             
            message_surface = pygame.Surface((screen.get_width(), line_height * len(lines)), pygame.SRCALPHA)

            # Render each line and blit it onto the message surface
            for i, line in enumerate(lines):
                line_surface = font.render(line, True, Colors.orange if i == 2 else Colors.yellow)
                line_rect = line_surface.get_rect(center=(screen.get_width() // 2, line_height * i))
                message_surface.blit(line_surface, line_rect)

            # Blit the message surface onto the screen
            message_rect = message_surface.get_rect(center=(screen.get_width() // 2, 155)) # Adjusted y-coordinate
            screen.blit(message_surface, message_rect)
         
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    game_start_date = datetime.now().strftime("%A %d/%m/%Y %H:%M:%S:%f")
                    self.total_game_start_time_ms = int(time.time() * 1000)
                    self.game_start_time_ms = int(time.time() * 1000)
                    self.level_change_time = time.time() # Initialize the level change timer
                    start_level_notice_timer = time.time()
                    level_notice_timer = 5
                    
                    # Send the event marker to iMotions on starting the game
                    string_for_iMotions = f"M;1;0;0;StartGame;Player started a new game\r\n"
                    print(f"Sending: {string_for_iMotions} to Port: {api.UDP_PORT}")
                    sys.stdout.flush()
                    time.sleep(0.001)

                    api.send_event_marker("StartGame", "Player started a new game")
                    api.send_scene_start(self.level + "Level")  # Automatically becomes e.g., "EasyLevel"


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
                                           "Starting speed": config.current_speed_timer,
                                            "Selected settings": {
                                            "Time Limit": str(config.find_skill_level_timer_minutes)+ " min " + str(config.find_skill_level_timer_seconds) + " s",
                                            "Starting level speeds": {"Easy start speed": config.easy_starting_speed,
                                            "Medium start speed": config.medium_starting_speed,
                                            "Hard start speed": config.hard_starting_speed},
                                            "Maximum level speeds": {"Easy max speed": config.easy_max_speed,
                                            "Medium max speed": config.medium_max_speed,
                                            "Hard max speed": config.hard_max_speed},
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

    def time_over_screen(self):
        global grid_width, grid_height
        global column_cell_size, row_cell_size
        global scale_w, scale_h
        global scale_x, scale_y

        game_status = "Time ended"
        self.write_end_game_data(game_status)

        
        self.game_over = False
        
        end_time_limit = 3      # show endscreen for 3 seconds
        end_screen_start_time = time.time()     # to start the timer
        show_end_timer = True




        while show_end_timer:
            # rect
            end_timer_rect = pygame.Rect(column_cell_size * 1 + 11, row_cell_size * 5 + 11, column_cell_size * 8, row_cell_size * 4)
            pygame.draw.rect(screen, Colors.soft_blue, end_timer_rect)

            # text1
            size = int(column_cell_size * 1.4)
            time_ended_font = pygame.font.Font(None, size)
            time_over_surface1 = time_ended_font.render("Time", True, Colors.dark_grey)
            screen.blit(time_over_surface1, time_over_surface1.get_rect(centerx = end_timer_rect.centerx, centery = end_timer_rect.centery * 0.9))

            # text3
            time_over_surface2 = time_ended_font.render("has ended", True, Colors.dark_grey)
            screen.blit(time_over_surface2, time_over_surface1.get_rect(centerx = end_timer_rect.centerx * 0.75, centery = end_timer_rect.centery * 1.05))

            screen.blit(screen, (scale_x, scale_y))
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

                if event.type == pygame.VIDEORESIZE:
                    scale_w = 500.0 + ((event.h - 625.0))
                    scale_h = 625.0 + ((event.h - 625.0))

                    scale_x = (event.w - scale_w) / 2.0
                    scale_y = 1.0
                    
                    self.draw_during_run()
        
        pygame.quit()
        sys.exit()

    def time_over_screen(self,main_menu):
        game_status = "Time ended"
        self.write_end_game_data(game_status)

        self.game_over = False

        end_time_limit = 3
        end_screen_start_time = time.time()
        show_end_timer = True

        while show_end_timer:
            pygame.draw.rect(screen, Colors.soft_blue, pygame.Rect(100, 260, 320, 40))
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

                if event.type == pygame.VIDEORESIZE:
                    scale_w = 500.0 + ((event.h - 625.0))
                    scale_h = 625.0 + ((event.h - 625.0))

                    scale_x = (event.w - scale_w) / 2.0
                    scale_y = 1.0
                    
                    self.draw_during_run()
        try:

            # Remote control command to iMotions
            string_for_iMotions = f"R;2;;SLIDESHOWNEXT\r\n"
            sendtcp(string_for_iMotions)
            print(f"Sending: {string_for_iMotions} to Port: {api.TCP_PORT}")
            sys.stdout.flush()
            time.sleep(0.001)
        except Exception as e:
            print(f"Failed to send TCP message: {e}")

        string_for_iMotions = f"M;2;;;GameClose;Game was closed;D;\r\n"
        sendudp(string_for_iMotions)
        print(f"Sending: {string_for_iMotions} to Port: {api.UDP_PORT}")
        sys.stdout.flush()
        time.sleep(0.001)       
        return_to_main_menu(screen, main_menu)

    def true_game_over_screen(self):
        true_end_time_limit = 3     # show true game over screen for 3 seconds
        true_end_screen_start_time = time.time()    # to start the timer
        true_end_timer = True

        while true_end_timer:
            true_end_screen_elapsed_time = time.time() - true_end_screen_start_time
        
            pygame.draw.rect(screen, Colors.soft_blue, pygame.Rect(30, 250, 400, 100))         
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
                    self.write_data(game_data)
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
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    # draws blocks on the screen (last code when drawing) on the ganme)
    def draw(self, screen):
        self.grid.draw(screen)
        if self.current_block != "Nothing": # doesn't draw the block if it doesn't fit
            self.current_block.draw(screen, 11, 11) # draws the current block

        if config.show_next_block:
            if self.next_block.id == 3:
                self.next_block.draw(screen, 255, 350)
            elif self.next_block.id == 4:
                self.next_block.draw(screen, 255, 340)
            else:
                self.next_block.draw(screen, 270, 330)
        
        """ if self.show_level_change == True:
            # Easy - Level
            if self.current_max_speed == config.easy_max_speed:
                notice_text = config.title_font.render("Level - Easy", True, Colors.white)
                screen.blit(notice_text, (80, 110))

                if (time.time() - start_level_notice_timer) >= level_notice_timer:
                    self.show_level_change = False

            # Medium - Level
            if self.current_max_speed == config.medium_max_speed:
                notice_text = config.title_font.render("Level - Medium", True, Colors.white)
                screen.blit(notice_text, (60, 110))

                if (time.time() - start_level_notice_timer) >= level_notice_timer:
                    self.show_level_change = False

            # Hard - Level
            if self.current_max_speed == config.hard_max_speed:
                notice_text = config.title_font.render("Level - Hard", True, Colors.white)
                screen.blit(notice_text, (80, 110))

                if (time.time() - start_level_notice_timer) >= level_notice_timer:
                    self.show_level_change = False """

    def draw_during_run(self,elapsed_time):
        screen.fill(Colors.dark_blue)

        if config.show_score:
            score_rect = pygame.Rect(320, 55, 170, 60)
            pygame.draw.rect(screen, Colors.dark_grey, score_rect, 0, 10)
            score_surface = config.title_font.render("Score", True, Colors.white)
            screen.blit(score_surface, (365, 20))
            score_value_surface = config.title_font.render(str(self.score), True, Colors.white)
            screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))

        if config.show_line_clears:
            line_clears_rect = pygame.Rect(320, 175, 170, 60)
            pygame.draw.rect(screen, Colors.dark_grey, line_clears_rect, 0, 10)
            line_clears_surface = config.guide_font.render("Lines Cleared", True, Colors.white)
            screen.blit(line_clears_surface, (330, 140))
            lines_cleared_nums = config.title_font.render(str(self.total_line_clears), True, Colors.white)
            screen.blit(lines_cleared_nums, (397, 190))

        if config.show_next_block:
            next_rect = pygame.Rect(320, 290, 170, 160)
            pygame.draw.rect(screen, Colors.dark_grey, next_rect, 0, 10)
            next_surface = config.title_font.render("Next", True, Colors.white)
            screen.blit(next_surface, (375, 255))

        if config.show_timer:
            player_timer_rect = pygame.Rect(320, 500, 170, 90)
            pygame.draw.rect(screen, Colors.dark_grey, player_timer_rect, 0, 10)
            if self.current_dificulty == "Base":
                player_timer_surface = config.title_font.render(str((config.base_time_limit - int(elapsed_time))), True, Colors.white)
            elif self.current_dificulty == "Find Skill Level":
                player_timer_surface = config.title_font.render(str((config.find_skill_level_time_limit - int(elapsed_time))), True, Colors.white)
            else:
                player_timer_surface = config.title_font.render(str((config.time_limit - int(elapsed_time))), True, Colors.white)
            screen.blit(player_timer_surface, player_timer_surface.get_rect(centerx=player_timer_rect.centerx, centery=player_timer_rect.centery))
            player_timer = config.title_font.render("Timer", True, Colors.white)
            screen.blit(player_timer, (365, 465))

        self.draw(screen)
        pygame.display.update()