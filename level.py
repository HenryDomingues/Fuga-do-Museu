from pathlib import Path

import pygame

from items import Artifact, TemporalFragment
from npc import Historian


class EgyptLevel:
    WIDTH = 3600
    GROUND_Y = 600

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.background = self.load_background()
        self.artifact = Artifact(300, self.GROUND_Y)
        self.historian = Historian(
            920,
            self.GROUND_Y,
            "Nardi",
            [
                "Nardi: Estes simbolos falam sobre o ciclo do Nilo.",
                "Nardi: O fragmento deve estar na camara antiga.",
            ],
        )
        self.fragment = TemporalFragment(3150, self.GROUND_Y)
        self.puzzle_solved = False
        self.hieroglyph_order = [1, 2, 3]
        self.puzzle_input = []
        self.message = ""
        self.message_timer = 0

    def load_background(self):
        paths = [
            self.project_root / "assets" / "backgrounds" / "gallery_portraits.png",
            self.project_root / "assets" / "backgrounds" / "gallery_portraits.jpg",
        ]
        for path in paths:
            if path.exists():
                try:
                    image = pygame.image.load(str(path)).convert()
                    if image.get_width() < self.WIDTH:
                        image = pygame.transform.smoothscale(image, (self.WIDTH, 720))
                    return image
                except pygame.error as error:
                    print(f"ERRO ao carregar asset {path}: {error}")
        print("ERRO: cenario do Egito ausente; usando placeholder visual.")
        image = pygame.Surface((self.WIDTH, 720))
        image.fill((84, 58, 34))
        return image

    def reset(self):
        self.artifact.activated = False
        self.fragment.collected = False
        self.puzzle_solved = False
        self.puzzle_input.clear()
        self.message = ""
        self.message_timer = 0

    def set_message(self, text, seconds=3):
        self.message = text
        self.message_timer = int(seconds * 60)

    def interact(self, player):
        if self.artifact.rect.colliderect(player.rect.inflate(90, 30)) and not self.artifact.activated:
            self.artifact.activated = True
            self.set_message("O artefato reconheceu o toque de Danas.")
            return "artifact"
        if self.historian.near(player):
            self.set_message(self.historian.lines[0 if not self.historian.talked else 1])
            self.historian.talked = True
            return "dialogue"
        if 1800 < player.rect.centerx < 2150 and not self.puzzle_solved:
            self.set_message("Observe os hieroglifos e pressione 1, 2 e 3.")
            return "puzzle"
        return None

    def puzzle_key(self, key):
        if self.puzzle_solved:
            return
        if key in (pygame.K_1, pygame.K_2, pygame.K_3):
            value = key - pygame.K_0
            self.puzzle_input.append(value)
            if self.puzzle_input != self.hieroglyph_order[:len(self.puzzle_input)]:
                self.puzzle_input.clear()
                self.set_message("A ordem esta errada. Observe novamente.")
            elif len(self.puzzle_input) == len(self.hieroglyph_order):
                self.puzzle_solved = True
                self.set_message("O mecanismo antigo foi aberto.")

    def update(self):
        self.fragment.update()
        if self.message_timer > 0:
            self.message_timer -= 1

    def draw(self, surface, camera_x, player):
        surface.fill((13, 10, 12))
        surface.blit(self.background, (-int(camera_x), 0))
        world = pygame.Surface((self.WIDTH, 720), pygame.SRCALPHA)
        pygame.draw.rect(world, (12, 10, 8, 85), (0, 0, self.WIDTH, 150))
        pygame.draw.rect(world, (34, 23, 15, 125), (0, self.GROUND_Y, self.WIDTH, 120))
        pygame.draw.line(world, (139, 104, 57, 190), (0, self.GROUND_Y), (self.WIDTH, self.GROUND_Y), 3)
        surface.blit(world, (-int(camera_x), 0))
        self.artifact.draw(surface, camera_x)
        self.historian.draw(surface, camera_x)
        self.fragment.draw(surface, camera_x)
        player.draw(surface, camera_x)
        if 1800 < player.rect.centerx < 2150 and not self.puzzle_solved:
            x = 1960 - int(camera_x)
            pygame.draw.rect(surface, (32, 22, 14), (x - 160, 180, 320, 125), border_radius=7)
            pygame.draw.rect(surface, (204, 157, 78), (x - 160, 180, 320, 125), 3, border_radius=7)
            for index, symbol in enumerate(("1", "2", "3")):
                text = pygame.font.Font(None, 42).render(symbol, True, (241, 211, 131))
                surface.blit(text, (x - 105 + index * 80, 220))


class GreeceLevel:
    WIDTH = 3600
    GROUND_Y = 600

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.background = self.load_background()
        self.fragment = TemporalFragment(3050, self.GROUND_Y)
        self.puzzle_solved = True
        self.message = ""
        self.message_timer = 0

    def load_background(self):
        path = self.project_root / "assets" / "backgrounds" / "fundo_fase2.jpg"
        if path.exists():
            try:
                image = pygame.image.load(str(path)).convert()
                if image.get_width() < self.WIDTH:
                    image = pygame.transform.smoothscale(image, (self.WIDTH, 720))
                return image
            except pygame.error as error:
                print(f"ERRO ao carregar asset {path}: {error}")
        print(f"ERRO: asset ausente: {path}")
        image = pygame.Surface((self.WIDTH, 720))
        image.fill((38, 48, 62))
        return image

    def reset(self):
        self.fragment.collected = False
        self.message = ""
        self.message_timer = 0

    def update(self):
        self.fragment.update()
        if self.message_timer > 0:
            self.message_timer -= 1

    def interact(self, player):
        if self.fragment.rect.colliderect(player.rect.inflate(100, 20)):
            self.message = "O fragmento grego esta ao alcance."
            self.message_timer = 180
            return "fragment"
        return None

    def puzzle_key(self, key):
        return None

    def draw(self, surface, camera_x, player):
        surface.fill((12, 14, 20))
        surface.blit(self.background, (-int(camera_x), 0))
        world = pygame.Surface((self.WIDTH, 720), pygame.SRCALPHA)
        pygame.draw.rect(world, (8, 10, 16, 70), (0, 0, self.WIDTH, 150))
        pygame.draw.rect(world, (25, 27, 34, 120), (0, self.GROUND_Y, self.WIDTH, 120))
        pygame.draw.line(world, (161, 143, 100, 180), (0, self.GROUND_Y), (self.WIDTH, self.GROUND_Y), 3)
        surface.blit(world, (-int(camera_x), 0))
        self.fragment.draw(surface, camera_x)
        player.draw(surface, camera_x)


class HistoricalLevel:
    WIDTH = 3600
    GROUND_Y = 600

    def __init__(self, project_root, level_id):
        self.project_root = Path(project_root)
        self.level_id = level_id
        self.background = self.load_background()
        self.fragment = TemporalFragment(3050, self.GROUND_Y)
        self.puzzle_solved = True
        self.message = ""
        self.message_timer = 0

    def load_background(self):
        path = self.project_root / "assets" / "backgrounds" / f"fundo_fase{self.level_id}.jpg"
        if path.exists():
            try:
                image = pygame.image.load(str(path)).convert()
                if image.get_width() < self.WIDTH:
                    image = pygame.transform.smoothscale(image, (self.WIDTH, 720))
                return image
            except pygame.error as error:
                print(f"ERRO ao carregar asset {path}: {error}")
        print(f"ERRO: asset ausente: {path}")
        image = pygame.Surface((self.WIDTH, 720))
        image.fill((35, 35, 42))
        return image

    def reset(self):
        self.fragment.collected = False
        self.message = ""
        self.message_timer = 0

    def update(self):
        self.fragment.update()
        if self.message_timer > 0:
            self.message_timer -= 1

    def interact(self, player):
        if self.fragment.rect.colliderect(player.rect.inflate(100, 20)):
            self.message = f"Fragmento da fase {self.level_id} encontrado."
            self.message_timer = 180
            return "fragment"
        return None

    def puzzle_key(self, key):
        return None

    def draw(self, surface, camera_x, player):
        surface.fill((12, 12, 16))
        surface.blit(self.background, (-int(camera_x), 0))
        world = pygame.Surface((self.WIDTH, 720), pygame.SRCALPHA)
        pygame.draw.rect(world, (8, 8, 12, 70), (0, 0, self.WIDTH, 150))
        pygame.draw.rect(world, (25, 25, 30, 120), (0, self.GROUND_Y, self.WIDTH, 120))
        pygame.draw.line(world, (150, 130, 95, 180), (0, self.GROUND_Y), (self.WIDTH, self.GROUND_Y), 3)
        surface.blit(world, (-int(camera_x), 0))
        self.fragment.draw(surface, camera_x)
        player.draw(surface, camera_x)
