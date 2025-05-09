from colors import Colors
import pygame
from position import Position

class Block:
    def __init__(self,id):
        self.id = id
        self.cells = {}         # dictionary, to store occupied cells in the bounding grid for each rotation state of the block
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0 
        self.colors = Colors.get_cell_colors()      # colors of the occupied cells

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns 

    # get the current position of the block in the grid
    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]   
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles
    
    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0     # to loop rotation state back to the start of the rotation-state-list

    def undo_rotation(self):
            self.rotation_state -= 1
            if self.rotation_state == -1:
                self.rotation_state = len(self.cells)-1 # to loop rotation state back to the end of the rotation-state-list

    # draws block tiles on the grid           
    def draw(self, screen, offset_x, offset_y):   
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column *self.cell_size, offset_y + tile.row *self.cell_size, self.cell_size -1, self.cell_size -1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

    # These settings determine how big the next-block's tiles are on the right side of the screen
    """ def draw_next_block(self, screen, offset_x, offset_y):  
        next_block_size = data_width * 0.175
        tiles = self.get_cell_positions()

        for tile in tiles:
            tile_rect = pygame.Rect(tile.column * next_block_size - offset_x - 3, offset_y + tile.row *next_block_size -3, next_block_size - 1, next_block_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

     """

    
