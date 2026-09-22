import pygame


class Historian:
    def __init__(self, x, ground_y, name, lines):
        self.name = name
        self.lines = lines
        self.rect = pygame.Rect(x, ground_y - 120, 54, 120)
        self.talked = False

    def near(self, player):
        return self.rect.colliderect(player.rect.inflate(90, 20))

    def draw(self, surface, camera_x):
        x = self.rect.x - int(camera_x)
        y = self.rect.y
        pygame.draw.ellipse(surface, (22, 16, 12), (x - 5, y + 102, 66, 24))
        pygame.draw.rect(surface, (150, 103, 51), (x + 7, y + 42, 40, 73), border_radius=6)
        pygame.draw.circle(surface, (151, 94, 64), (x + 27, y + 25), 22)
        pygame.draw.rect(surface, (28, 20, 16), (x + 4, y + 4, 47, 16), border_radius=6)
