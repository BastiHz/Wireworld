import pygame

from src import constants


class Camera:
    def __init__(self, window_size, cell_width, cell_size, cells):
        self.window_width, self.window_height = window_size
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Wireworld")
        self.cells = cells
        self.cell_width = cell_width
        self.cell_size = cell_size
        self.mouse_grid_position = (0, 0)
        self.mouse_rect = pygame.Rect(self.mouse_grid_position, cell_size)
        self.mouse_screen_position = pygame.Vector2()
        self.position = pygame.Vector2()
        self.rect = self.window.get_rect()
        self.rect_for_cell_drawing = self.rect.copy()
        self.keyboard_scoll_direction = pygame.Vector2()
        self.keyboard_scroll_speed = pygame.Vector2(constants.KEYBOARD_SCROLL_SPEED)
        self.mouse_movement_rel = pygame.Vector2()
        self.scroll_amount = pygame.Vector2()

        self.show_debug_info = False
        self.n_visible_cells = 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self.show_debug_info = not self.show_debug_info
            elif event.key == pygame.K_w:
                self.keyboard_scoll_direction.y += 1
            elif event.key == pygame.K_a:
                self.keyboard_scoll_direction.x += 1
            elif event.key == pygame.K_s:
                self.keyboard_scoll_direction.y -= 1
            elif event.key == pygame.K_d:
                self.keyboard_scoll_direction.x -= 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.keyboard_scoll_direction.y -= 1
            elif event.key == pygame.K_a:
                self.keyboard_scoll_direction.x -= 1
            elif event.key == pygame.K_s:
                self.keyboard_scoll_direction.y += 1
            elif event.key == pygame.K_d:
                self.keyboard_scoll_direction.x += 1
        elif event.type == pygame.MOUSEMOTION and event.buttons[2]:  # 2 = right mouse button
            self.mouse_movement_rel += event.rel
        elif event.type == pygame.MOUSEWHEEL:
            print(event)
            # TODO: Collect all wheel events of a frame before performing the zoom in update().

    def update(self, dt):
        # I collect all scrolling and zooming events before updating the camera
        # because there often are multiple such events per frame.
        self.scroll(
            self.mouse_movement_rel
            + self.keyboard_scoll_direction.elementwise()
            * self.keyboard_scroll_speed
            * dt
        )

        self.update_mouse_position()

    def scroll(self, rel):
        if rel != (0, 0):
            self.position -= rel
            self.rect.topleft = self.position
            # TODO: Should scroll speed depend on zoom level?
            for cell in self.cells.values():
                cell.update_screen_position()
            self.mouse_movement_rel.update(0, 0)

    def zoom(self):
        # TODO: Implement this. With mouse wheel and keyboard.
        pass

    def update_mouse_position(self):
        self.mouse_screen_position.update(pygame.mouse.get_pos())
        grid_position = (self.mouse_screen_position + self.rect.topleft) // self.cell_width
        self.mouse_grid_position = tuple(grid_position)
        self.mouse_rect.topleft = (grid_position * self.cell_width - self.rect.topleft)

    def world_to_screen_position(self, world_x, world_y):
        return world_x - self.rect.x, world_y - self.rect.y

    def draw(self):
        self.window.fill(constants.BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_cells()
        pygame.draw.rect(self.window, constants.MOUSE_HIGHLIGHT_COLOR, self.mouse_rect, 1)
        if self.show_debug_info:
            self.draw_debug_info()
        pygame.display.flip()

    def draw_grid(self):
        for x in range(self.cell_width - (self.rect.x % self.cell_width),
                       self.rect.width,
                       self.cell_width):
            pygame.draw.line(self.window, constants.GRID_COLOR, (x, 0), (x, self.window_height))

        for y in range(self.cell_width - (self.rect.y % self.cell_width),
                       self.rect.height,
                       self.cell_width):
            pygame.draw.line(self.window, constants.GRID_COLOR, (0, y), (self.window_width, y))

    def draw_cells(self):
        visible_cells = self.rect_for_cell_drawing.collidedictall(self.cells, True)
        for _, cell in visible_cells:
            self.window.blit(cell.image, cell.rect)
        self.n_visible_cells = len(visible_cells)

    def draw_debug_info(self):
        pygame.draw.circle(self.window, (255, 0, 0), self.world_to_screen_position(0, 0), 3)
        constants.DEBUG_FONT.render_to(
            self.window,
            constants.DEBUG_MARGIN,
            f"mouse grid position: {self.mouse_grid_position}"
        )
        constants.DEBUG_FONT.render_to(
            self.window,
            constants.DEBUG_MARGIN + constants.DEBUG_LINE_SPACING,
            f"mouse rect screen position: {self.mouse_rect.topleft}"
        )
        constants.DEBUG_FONT.render_to(
            self.window,
            constants.DEBUG_MARGIN + constants.DEBUG_LINE_SPACING * 2,
            f"number of visible cells: {self.n_visible_cells}"
        )
