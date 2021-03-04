import pygame

from src import constants
from src.simulation import Simulation
from src.camera import Camera
from src.cell import Cell


def run(window_size, cell_width):
    pygame.init()
    cells = {}
    cell_size = (cell_width, cell_width)
    Cell.create_cell_images(cell_size)
    camera = Camera(window_size, cell_width, cell_size, cells)
    simulation = Simulation(camera, cell_width, cells)
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(constants.FPS)
        camera.update_mouse_position()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            simulation.process_event(event, dt)
            camera.process_event(event)
        simulation.update(dt)
        camera.draw()