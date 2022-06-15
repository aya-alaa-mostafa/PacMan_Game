import pygame
from settings import *
vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        # Starting from position x and y on the grid
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        # Set the direction 2d
        self.direction = vec(1, 0)
        # Store it for collect
        self.stored_direction = None
        # Movement
        self.able_to_move = True
        # For current Score
        self.current_score = 0
        # Speed of runnning
        self.speed = 2
        # Time for live
        self.lives = 1

    def update(self):
        # for updating any movement or collect
        if self.able_to_move:
            # If there is a chance for movement , move it like i += d*s
            self.pix_pos += self.direction*self.speed
        if self.time_to_move():
            # if time to move return 1 , store the movement on stored direction
            if self.stored_direction != None:
                # If empty , push the result
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        # Setting grid position in reference to pix position (POS)
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER + self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER + self.app.cell_height//2)//self.app.cell_height+1
        # Eating
        if self.on_coin():
            self.eat_coin()

    def draw(self):
        # Draw circle using colors and positions
        pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (int(self.pix_pos.x),
                                                            int(self.pix_pos.y)), self.app.cell_width//2-2)
        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (30 + 20*x, HEIGHT - 15), 7)

        # Drawing the grid pos rect
        # pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                         self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos[0]*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (self.grid_pos[1]*self.app.cell_height) +
                   TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)

        print(self.grid_pos, self.pix_pos)

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True
