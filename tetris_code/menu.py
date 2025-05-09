# A Menu which opens the Tetris game. It has buttons for each different level and a guide page.

import pygame
import pygame_menu
import os
from pygame_menu import Theme
from pygame_menu.locals import ALIGN_CENTER
from pygame_menu.widgets import MENUBAR_STYLE_SIMPLE
from colors import Colors
import config
import api
from api import sendudp
import sys
import time
import Base_Level
import Easy_Level
import Medium_Level
import Hard_Level
import credits


pygame.init()

screen = pygame.display.set_mode((500, 620))
config.current_dificulty = "Menu"
pygame.display.set_caption("Python Tetris - " + config.current_dificulty)

# Theme for the menu
my_theme = Theme(
    background_color=Colors.dark_blue,
    title_background_color=Colors.dark_blue,
    title_font_color=Colors.white,
    widget_font_color=Colors.yellow,
    selection_color=Colors.orange,
    title_font=pygame.font.Font(None, 60),
    widget_font=pygame.font.Font(None, 40),
    widget_margin=(0, 10),
    title_bar_style=MENUBAR_STYLE_SIMPLE,
    widget_alignment=ALIGN_CENTER
)

# Theme for the guide menu with smaller text
guide_theme = Theme(
    background_color=Colors.dark_blue,
    title_background_color=Colors.dark_blue,
    title_font_color=Colors.white,
    widget_font_color=Colors.yellow,
    selection_color=Colors.orange,
    title_font=pygame.font.Font(None, 50),  # Slightly smaller title font
    widget_font=pygame.font.Font(None, 20),  # Smaller widget font for guide text
    widget_margin=(0, 0),
    title_bar_style=MENUBAR_STYLE_SIMPLE,
    widget_alignment=ALIGN_CENTER
)
credits_theme = Theme(
    background_color=Colors.dark_blue,
    title_background_color=Colors.dark_blue,
    title_font_color=Colors.white,
    widget_font_color=Colors.yellow,
    selection_color=Colors.orange,
    title_font=pygame.font.Font(None, 55),  # Slightly smaller title font
    widget_font=pygame.font.Font(None, 30),  # Smaller widget font for guide text
    widget_margin=(0, 0),
    title_bar_style=MENUBAR_STYLE_SIMPLE,
    widget_alignment=ALIGN_CENTER
)

def start_level(module):
    module.main(main_menu)  # Pass main_menu to the level's main function

# Guide Menu, which opens from "Guide"-button
def create_guide_menu():
    guide_menu = pygame_menu.Menu('Guide', 500, 620, theme=guide_theme)
    
    image_path = os.path.join(os.path.dirname(__file__), 'assets', 'controls.png')
    guide_menu.add.image(image_path, scale=(0.58, 0.58))
    
    # Text instructions in Guide menu
    guide_text = [
        '',
        '1. Base Level:',
        '',
        '   - Get familiar with the game',  
        '   - Slowest level, no speed increases',
        '   - Play for 3 minutes and try to clear as many lines as possible',
        '',
        '2. Mental workload:',
        '',
        '   - If you cleared less than 10 lines -> Easy',
        '   - If you cleared between 10 and 20 lines -> Medium',
        '   - If you cleared more than 20 lines -> Hard',
        '   - If your skill  level is: Easy or Medium',
        '   - Play Easy level 10 min --> survey --> Medium level 10 min --> survey',
        '',
        '   - If your skill  level is: Hard',
        '   - Play Medium level 10 min --> survey --> Hard level 10 min --> survey',
        ''
    ]
    
    for line in guide_text:
        guide_menu.add.label(line, align=pygame_menu.locals.ALIGN_LEFT)

    # Back button from Guide menu
    guide_menu.add.button('Back', pygame_menu.events.BACK)

    guide_menu.add.label('')  # Empty space
    
    return guide_menu
def create_credit_menu():
    credit_menu = pygame_menu.Menu('Credits', 500, 620, theme=credits_theme)
    credits_text = credits.credits_text
    
    for line in credits_text:
        credit_menu.add.label(line, align=pygame_menu.locals.ALIGN_CENTER)
    credit_menu.add.button('Back', pygame_menu.events.BACK)
    return credit_menu

# Main Menu
def main_menu():
    menu = pygame_menu.Menu('EEG Tetris', 500, 620, theme=my_theme)

    menu.add.button('Base Level', lambda: start_level(Base_Level))
   # menu.add.button('Find Skill Level', lambda: start_level(Find_Skill_Level))
    menu.add.button('Easy', lambda: start_level(Easy_Level))
    menu.add.button('Medium', lambda: start_level(Medium_Level))
    menu.add.button('Hard', lambda: start_level(Hard_Level))
    
    menu.add.button('Guide', create_guide_menu())
    menu.add.button('Credits', create_credit_menu())

    menu.add.button('Quit', pygame_menu.events.EXIT)

    return menu

if __name__ == "__main__":
    menu = main_menu()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                string_for_iMotions = f"M;2;;;MenuClose;Menu was closed;D;\r\n"
                sendudp(string_for_iMotions)
                print(f"Sending: {string_for_iMotions} to Port: {api.UDP_PORT}")
                sys.stdout.flush()
                time.sleep(0.001)
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                menu.resize(event.w, event.h)
                menu.center_content()

        screen.fill(Colors.dark_blue)
        menu.update(events)
        menu.draw(screen)
        pygame.display.flip()

    pygame.quit()