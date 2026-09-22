from pathlib import Path

import pygame


PROJECT_ROOT = Path(__file__).resolve().parent


class Player:
    def __init__(self, x, ground_y):
        self.rect = pygame.Rect(x, ground_y - 180, 72, 180)
        self.ground_y = ground_y
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.72
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.moving = False
        self.current_frame = 0
        self.animation_timer = 0
        self.frames = self.load_character_images()
        self.image = self.frames[0]

    def load_character_images(self):
        image_path = PROJECT_ROOT / "assets" / "characters" / "danas" / "Danas_walk.png"
        try:
            source = pygame.image.load(str(image_path)).convert_alpha()
        except (pygame.error, FileNotFoundError):
            print(f"ERRO: asset ausente: {image_path}")
            return [self.fallback_image()]

        if source.get_width() / max(1, source.get_height()) > 2.0:
            columns = 8
            rows = 2
            frame_width = source.get_width() // columns
            frame_height = source.get_height() // rows
            frames = []
            for row in range(rows):
                for column in range(columns):
                    frame = source.subsurface(
                        pygame.Rect(
                            column * frame_width,
                            row * frame_height,
                            frame_width,
                            frame_height,
                        )
                    ).copy()
                    frames.append(self.prepare_image(frame))
            return frames

        return [self.prepare_image(source)]

    def prepare_image(self, image):

        for pixel_y in range(image.get_height()):
            for pixel_x in range(image.get_width()):
                red, green, blue, _ = image.get_at((pixel_x, pixel_y))
                if max(red, green, blue) - min(red, green, blue) < 12 and min(red, green, blue) > 150:
                    image.set_at((pixel_x, pixel_y), (red, green, blue, 0))

        bounds = image.get_bounding_rect(min_alpha=10)
        if bounds.width == 0 or bounds.height == 0:
            return self.fallback_image()

        image = image.subsurface(bounds).copy()
        max_height = 180
        scale = max_height / image.get_height()
        return pygame.transform.smoothscale(
            image,
            (max(1, int(image.get_width() * scale)), max_height)
        )

    @staticmethod
    def fallback_image():
        image = pygame.Surface((64, 128), pygame.SRCALPHA)
        pygame.draw.circle(image, (166, 103, 73), (32, 25), 18)
        pygame.draw.rect(image, (61, 83, 55), (12, 43, 40, 47), border_radius=6)
        pygame.draw.rect(image, (45, 53, 68), (15, 88, 13, 36))
        pygame.draw.rect(image, (45, 53, 68), (36, 88, 13, 36))
        pygame.draw.rect(image, (15, 15, 18), (14, 8, 36, 15), border_radius=7)
        return image

    def update(self, keys, world_width):
        self.moving = False
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing_right = False
            self.moving = True
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing_right = True
            self.moving = True

        self.rect.x = max(0, min(self.rect.x, world_width - self.rect.width))

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        self.velocity_y += self.gravity
        self.rect.y += int(self.velocity_y)
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.velocity_y = 0
            self.on_ground = True

        if self.moving and self.on_ground and len(self.frames) > 1:
            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
        else:
            self.current_frame = 0
            self.animation_timer = 0
        self.image = self.frames[self.current_frame]

    def draw(self, surface, camera_x):
        image = self.image
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)
        image_rect = image.get_rect(
            midbottom=(self.rect.centerx - int(camera_x), self.rect.bottom)
        )
        surface.blit(image, image_rect)
