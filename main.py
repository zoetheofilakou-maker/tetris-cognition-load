import os
import pygame
import sys
import time
import config
from game import Game 
from colors import Colors  
import api
from api import sendudp
from utils import return_to_main_menu
from api import send_event_marker,send_scene_start, send_scene_end, send_score_update, send_level_update, send_line_clear_summary


print("main.py started")

pygame.init()
print("Pygame initialized")

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("EEG Tetris")
print("Game window created")

# Optional: a simple display before the real game starts (can remove later)
screen.fill((0, 0, 0))
pygame.display.flip()

def run_game(main_menu):
    elapsed_time = 0

    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height))
    scale_x = 1.0
    scale_y = 1.0

    scale_w = 500
    scale_h = 620

    pygame.display.set_caption("Python Tetris - " + config.current_dificulty)

    clock = pygame.time.Clock()
    current_speed = pygame.USEREVENT
    current_speed_timer = config.current_starting_speed  
    pygame.time.set_timer(current_speed, current_speed_timer)

    game = Game(current_speed, config.current_starting_speed, config.current_max_speed, config.speed_increasement, config.current_dificulty, config.current_dificulty)

    if config.current_dificulty == "Base":
        current_speed_timer = config.base_starting_speed
        send_scene_start(config.current_dificulty + "Level")

    elif config.current_dificulty == "Easy":
        current_speed_timer = config.easy_starting_speed
        send_scene_start(config.current_dificulty + "Level")

    elif config.current_dificulty == "Medium":
        current_speed_timer = config.medium_starting_speed
        send_scene_start(config.current_dificulty + "Level")

    elif config.current_dificulty == "Hard":
        current_speed_timer = config.hard_starting_speed
        send_scene_start(config.current_dificulty + "Level")


    pygame.time.set_timer(current_speed, current_speed_timer)

    change_level = pygame.USEREVENT + 1
    change_level_timer = (config.level_minutes * 60 * 1000) + (config.level_seconds * 1000)
    pygame.time.set_timer(change_level, change_level_timer)

    time_limit = (config.timer_minutes * 60 + config.timer_seconds)

    current_max_speed = config.current_max_speed

    start_screen = True
    block_moved_down = False

    while True:
        for event in pygame.event.get():
            if start_screen:
                game.waiting_screen()
                start_screen = False
                start_time = time.time()
                send_event_marker("StartGame", "Player started the game")
                send_scene_start(config.current_dificulty + "Level")
                game.show_level_change = True

            elapsed_time = time.time() - start_time

            if elapsed_time >= time_limit:
                send_score_update(game.score)
                send_level_update(game.level)
                send_line_clear_summary(game.total_line_clears)
                send_scene_end(config.current_dificulty + "Level")
                game.time_over_screen(main_menu)

            if event.type == pygame.QUIT:
                game_data = {"Cause of game ending": "Pressed quit during game play"}
                game.write_data(game_data)
                game_status = "Quit"
                game.write_end_game_data(game_status)
                pygame.quit()
                sys.exit()

            if game.game_over:
                block_moved_down = False
                game_status = "Game Over"
                game.write_end_game_data(game_status)

                while game.game_over:
                    elapsed_time = time.time() - start_time
                    game.game_over_screen()

                    if elapsed_time >= time_limit:
                        game.time_over_screen(main_menu)

                    player_timer_rect2 = pygame.Rect(screen_width / 2, screen_height, 170, 90)
                    pygame.draw.rect(screen, Colors.light_blue, player_timer_rect2, 0, 10)

                    player_timer_surface = config.title_font.render(str((time_limit - int(elapsed_time))), True, Colors.white)
                    screen.blit(player_timer_surface, player_timer_surface.get_rect(centerx=player_timer_rect2.centerx, centery=player_timer_rect2.centery))

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_data = {"Cause of game ending": "Pressed quit at the game over screen"}
                            game.write_data(game_data)
                            pygame.quit()
                            sys.exit()

                        if event.type == pygame.KEYDOWN:
                            game_status = {"Time": int(time.time() * 1000) - game.total_game_start_time_ms,
                                           "Game reset": "Game started again after game over"}
                            game.write_data(game_status)
                            game.game_over = False
                game.reset()
                game.write_block_data()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not game.game_over:
                    game.move_left()
                if event.key == pygame.K_RIGHT and not game.game_over:
                    game.move_right()
                if event.key == pygame.K_SPACE and not game.game_over:
                    game.hard_drop()
                if event.key == pygame.K_DOWN and not game.game_over:
                    game.move_down()
                if event.key == pygame.K_UP and not game.game_over:
                    game.rotate()
                if event.key == pygame.K_ESCAPE:
                    game_data = {"Cause of game ending": "Pressed escape during game play"}
                    string_for_iMotions = f"M;2;;;GameClose;Game was closed;D;\r\n"
                    sendudp(string_for_iMotions)
                    print(f"Sending: {string_for_iMotions} to Port: {api.UDP_PORT}")
                    sys.stdout.flush()
                    time.sleep(0.001)
                    game.write_data(game_data)
                    game_status = "Quit"
                    game.write_end_game_data(game_status)
                    return_to_main_menu(screen, main_menu)

            if event.type == current_speed and not game.game_over:
                game.move_down()

            if event.type == pygame.VIDEORESIZE:
                scale_w = 500.0 + ((event.h - 625.0))
                scale_h = 625.0 + ((event.h - 625.0))
                scale_x = (event.w - scale_w) / 2.0
                scale_y = 1.0

        game.draw_during_run(elapsed_time)
        clock.tick(60)

# ✅ Add this at the end to run the game
if __name__ == "__main__":
    run_game(main_menu=False)
