import pygame
from colors import Colors
import sys
import time
import api
from api import sendudp
from api import send_line_clear


class Grid:
    

    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30 # size of each cell of the grid in pixels
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)] # list comprehension to create lists of zeros
        self.colors = Colors.get_cell_colors() # creates the colors list

    # inside the grid
    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >=0 and column < self.num_cols:
            return True
        return False
    
    # if the cell is empty
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        
        # Send Standard Line clear event to iMotions
        send_line_clear()

        return True
        
    

    # goes through 1 row and clears all the tiles
    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    # after clearing full rows
    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    # goes through rows and clears full rows
    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    # draw the grid
    def draw(self,screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                if 0 <= cell_value <len(self.colors): #ensure cell_value is within the range if colors
                    cell_rect = pygame.Rect(column*self.cell_size +11,row * self.cell_size +11, self.cell_size -1,self.cell_size -1)
                    pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
                    pygame.draw.rect(screen, Colors.grid_line, cell_rect, 1) # draw the border of the cell