import pygame

def return_to_main_menu(screen, main_menu):
    main_menu_instance = main_menu()  # Initialize the main menu
    main_menu_instance.mainloop(screen)  # Display the main menu