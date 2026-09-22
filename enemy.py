import pygame


class Morten:
    def __init__(self, x, ground_y):
        self.rect = pygame.Rect(x, ground_y - 132, 58, 132)
        self.ground_y = ground_y
        self.speed = 2.2
        self.active = False

    def reset(self, x):
        self.rect.x = x
        self.rect.bottom = self.ground_y
        self.active = False

    def activate(self):
        self.active = True

    def update(self, target):
        if not self.active:
            return

        if self.rect.centerx < target.rect.centerx:
            self.rect.x += self.speed
        elif self.rect.centerx > target.rect.centerx:
            self.rect.x -= self.speed

    def touches(self, target):
        return self.active and self.rect.colliderect(target.rect.inflate(-18, -8))

    def draw(self, surface, camera_x):
        if not self.active:
            return

        x = self.rect.x - int(camera_x)
        y = self.rect.y
        pygame.draw.ellipse(surface, (12, 10, 14), (x - 8, y + 108, 74, 28))
        pygame.draw.rect(surface, (25, 22, 31), (x + 9, y + 48, 40, 76), border_radius=7)
        pygame.draw.circle(surface, (92, 67, 58), (x + 29, y + 30), 25)
        pygame.draw.rect(surface, (10, 10, 14), (x + 4, y + 5, 50, 20), border_radius=8)
        pygame.draw.circle(surface, (205, 166, 70), (x + 20, y + 31), 4)
        pygame.draw.circle(surface, (205, 166, 70), (x + 38, y + 31), 4)
