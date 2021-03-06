import pygame

from src.constants import *


class Cell:
    images = ()
    cells = {}

    @staticmethod
    def static_init(camera, cells):
        conductor_image = pygame.Surface(CELL_SIZE)
        conductor_image.fill(CONDUCTOR_COLOR)
        head_image = pygame.Surface(CELL_SIZE)
        head_image.fill(ELECTRON_HEAD_COLOR)
        tail_image = pygame.Surface(CELL_SIZE)
        tail_image.fill(ELECTRON_TAIL_COLOR)
        Cell.images = (conductor_image, head_image, tail_image)
        Cell.camera = camera
        Cell.cells = cells

    def __init__(self, camera):
        self.grid_position = camera.mouse_grid_position
        self.world_position = pygame.Vector2(self.grid_position) * CELL_WIDTH
        self.screen_position = pygame.Vector2()
        self.update_screen_position(camera.surface_rect.topleft)
        self.rect = pygame.Rect(self.world_position, CELL_SIZE)
        self.state = 0  # 0 = conductor, 1 = electron head, 2 = electron tail
        self.next_state = self.state
        self.image = Cell.images[self.state]
        self.neighbors = self.get_neighbors()

    def get_neighbors(self):
        neighbors = []
        x, y = self.grid_position
        for dx, dy in ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)):
            neighbor = Cell.cells.get((x + dx, y + dy), None)
            if neighbor is not None:
                neighbors.append(neighbor)
                neighbor.neighbors.append(self)
        return neighbors

    def prepare_update(self):
        if self.state == 0:
            # conductor -> electron head if one or two neighbors are electron heads
            n_neighbor_heads = sum(1 for neighbor in self.neighbors if neighbor.state == 1)
            if n_neighbor_heads in (1, 2):
                self.next_state = 1
            else:
                self.next_state = 0
        elif self.state == 1:
            # electron head -> electron tail
            self.next_state = 2
        else:
            # electron tail -> conductor
            self.next_state = 0

    def update_state(self):
        self.state = self.next_state
        self.image = Cell.images[self.state]

    def update_screen_position(self, surface_rect_position):
        self.screen_position = self.world_position - surface_rect_position

    def increment_state(self):
        self.state += 1
        if self.state > 2:
            self.delete()
        else:
            self.image = Cell.images[self.state]

    def remove_electricity(self):
        self.state = 0
        self.next_state = 0
        self.image = Cell.images[self.state]

    def delete(self):
        del Cell.cells[self.grid_position]
        for neighbor in self.neighbors:
            neighbor.neighbors.remove(self)
