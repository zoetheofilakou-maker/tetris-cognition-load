import pygame
import sys

print("Starting pygame test...")
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test Pygame Window")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 150))  # dark blue background
    pygame.display.flip()

pygame.quit()
sys.exit()
