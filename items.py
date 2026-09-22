import pygame


class TemporalFragment:
    def __init__(self, x, ground_y):
        self.rect = pygame.Rect(x, ground_y - 82, 34, 50)
        self.collected = False
        self.pulse = 0

    def update(self):
        self.pulse = (self.pulse + 3) % 360

    def collect_if_near(self, player):
        if not self.collected and self.rect.colliderect(player.rect.inflate(100, 20)):
            self.collected = True
            return True
        return False

    def draw(self, surface, camera_x):
        if self.collected:
            return
        x = self.rect.centerx - int(camera_x)
        y = self.rect.centery
        radius = 15 + int(abs(self.pulse - 180) / 30)
        pygame.draw.polygon(surface, (105, 220, 230), [(x, y - radius), (x + radius, y), (x, y + radius), (x - radius, y)])
        pygame.draw.polygon(surface, (220, 250, 255), [(x, y - radius + 7), (x + 5, y), (x, y + 7), (x - 5, y)])


class Artifact:
    def __init__(self, x, ground_y):
        self.rect = pygame.Rect(x, ground_y - 120, 72, 90)
        self.activated = False

    def draw(self, surface, camera_x):
        if self.activated:
            return
        x = self.rect.x - int(camera_x)
        pygame.draw.ellipse(surface, (22, 50, 58), (x, self.rect.y, 72, 90))
        pygame.draw.ellipse(surface, (80, 220, 220), (x + 12, self.rect.y + 12, 48, 66), 3)
        pygame.draw.circle(surface, (160, 250, 245), self.rect.center, 7)
