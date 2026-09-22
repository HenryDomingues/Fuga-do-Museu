from pathlib import Path
import sys

import pygame

from campaign import Campaign, ERAS
from dialogue import EGYPT_LINES, INTRO_LINES, Dialogue
from level import EgyptLevel, GreeceLevel, HistoricalLevel
from player import Player


PROJECT_ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT, FPS = 1280, 720, 60
BLACK = (8, 9, 12)
WHITE = (240, 240, 240)
GRAY = (155, 155, 155)
GOLD = (220, 170, 70)
CYAN = (93, 207, 214)
DARK = (20, 21, 28)

MENU = "menu"
STORY = "story"
ERA_SELECT = "era_select"
GAME = "game"
PAUSE = "pause"
SETTINGS = "settings"
COMPLETE = "complete"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FUGA DO MUSEU")
clock = pygame.time.Clock()
font_title = pygame.font.Font(None, 82)
font_heading = pygame.font.Font(None, 52)
font_button = pygame.font.Font(None, 34)
font_body = pygame.font.Font(None, 27)
font_small = pygame.font.Font(None, 22)

campaign = Campaign()
level = EgyptLevel(PROJECT_ROOT)
level_id = 1
player = Player(150, level.GROUND_Y)
state = MENU
story = Dialogue(INTRO_LINES + EGYPT_LINES)
story_mode = True
camera_x = 0.0
message = ""
message_timer = 0


class Button:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.hover = False

    def update(self):
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        fill = (53, 46, 35) if self.hover else DARK
        pygame.draw.rect(screen, fill, self.rect, border_radius=6)
        pygame.draw.rect(screen, GOLD, self.rect, 2, border_radius=6)
        text = font_button.render(self.label, True, WHITE)
        screen.blit(text, text.get_rect(center=self.rect.center))


play_button = Button(470, 270, 340, 58, "JOGAR")
continue_button = Button(470, 340, 340, 58, "CONTINUAR")
era_button = Button(470, 410, 340, 58, "EPOCAS")
settings_button = Button(470, 480, 340, 58, "CONFIGURACOES")
exit_button = Button(470, 550, 340, 58, "SAIR")
resume_button = Button(470, 350, 340, 58, "CONTINUAR")
menu_button = Button(470, 420, 340, 58, "MENU")


def show_message(text, seconds=3):
    global message, message_timer
    message = text
    message_timer = int(seconds * FPS)


def load_menu_background():
    path = PROJECT_ROOT / "assets" / "backgrounds" / "fundo_tela_inicial.jpg"
    if path.exists():
        try:
            image = pygame.image.load(str(path)).convert()
            scale = max(WIDTH / image.get_width(), HEIGHT / image.get_height())
            size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.smoothscale(image, size)
            crop = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            return image, crop
        except pygame.error as error:
            print(f"ERRO ao carregar asset {path}: {error}")
    print(f"ERRO: asset ausente: {path}")
    return None, pygame.Rect(0, 0, WIDTH, HEIGHT)


menu_background, menu_background_rect = load_menu_background()


def reset_egypt():
    global camera_x, story_mode, level, level_id
    level = EgyptLevel(PROJECT_ROOT)
    level_id = 1
    level.reset()
    player.rect.topleft = (150, level.GROUND_Y - player.rect.height)
    player.velocity_y = 0
    player.on_ground = True
    player.facing_right = True
    camera_x = 0
    story_mode = False


def start_level(selected_level):
    global level, level_id, camera_x, state
    if 2 <= selected_level <= 5 and campaign.is_unlocked(selected_level):
        if selected_level == 2:
            level = GreeceLevel(PROJECT_ROOT)
        else:
            level = HistoricalLevel(PROJECT_ROOT, selected_level)
        level_id = selected_level
        level.reset()
        player.rect.topleft = (150, level.GROUND_Y - player.rect.height)
        player.velocity_y = 0
        player.on_ground = True
        player.facing_right = True
        camera_x = 0
        state = GAME


def begin_story():
    global story, state, story_mode
    reset_egypt()
    story = Dialogue(INTRO_LINES + EGYPT_LINES)
    story_mode = True
    state = STORY


def centered(text, y, font=font_body, color=WHITE):
    surface = font.render(text, True, color)
    screen.blit(surface, surface.get_rect(center=(WIDTH // 2, y)))


def draw_menu():
    screen.fill(BLACK)
    if menu_background is not None:
        screen.blit(menu_background, menu_background_rect)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 7, 12, 145))
        screen.blit(overlay, (0, 0))
    else:
        pygame.draw.rect(screen, (18, 20, 28), (0, 0, WIDTH, HEIGHT))
    centered("FUGA DO MUSEU", 75, font_title)
    centered("UMA AVENTURA ATRAVES DA HISTORIA", 145, font_small, GRAY)
    play_button.draw()
    continue_button.draw()
    era_button.draw()
    settings_button.draw()
    exit_button.draw()
    centered(f"FRAGMENTOS TEMPORAIS  {len(campaign.fragments)}/10", 680, font_small, CYAN)


def draw_story():
    screen.fill((8, 10, 15))
    pygame.draw.rect(screen, (20, 23, 30), (115, 75, 1050, 570), 2)
    centered("A HISTORIA DA HUMANIDADE", 120, font_heading, GOLD)
    if not story.finished:
        centered(story.current, 350, font_body)
    centered("ENTER para continuar", 620, font_small, GRAY)


def draw_eras():
    screen.fill((10, 12, 17))
    centered("LINHA DO TEMPO", 70, font_title, GOLD)
    centered("Pressione 2, 3, 4 ou 5 para jogar uma epoca desbloqueada.", 125, font_small, GRAY)
    for index, era in enumerate(ERAS):
        y = 175 + index * 45
        unlocked = campaign.is_unlocked(era["id"])
        status = "OK" if era["id"] in campaign.fragments else ("ABERTA" if unlocked else "BLOQUEADA")
        color = CYAN if unlocked else (90, 90, 100)
        centered(f"{era['id']:02d}  {era['name']}  |  {era['period']}  |  {status}", y, font_small, color)
    centered("ESC para voltar", 675, font_small, GRAY)


def draw_settings():
    screen.fill(BLACK)
    centered("CONFIGURACOES", 150, font_title)
    centered("VOLUME       100%", 300, font_button)
    centered("TELA CHEIA   NAO", 360, font_button)
    centered("Audio e tela cheia serao conectados em uma proxima versao.", 450, font_small, GRAY)
    centered("ESC para voltar", 640, font_small, GRAY)


def draw_game():
    level.draw(screen, camera_x, player)
    hud = pygame.Surface((350, 102), pygame.SRCALPHA)
    hud.fill((7, 9, 13, 215))
    screen.blit(hud, (18, 18))
    era_name = ERAS[level_id - 1]["name"].upper()
    screen.blit(font_small.render(era_name, True, GOLD), (35, 31))
    screen.blit(font_small.render("DANAS   A/D mover   SPACE pular", True, WHITE), (35, 57))
    screen.blit(font_small.render("E investigar   ESC pausar", True, GRAY), (35, 80))
    if message_timer > 0:
        panel = pygame.Rect(220, 570, 840, 56)
        pygame.draw.rect(screen, (7, 9, 13), panel, border_radius=6)
        pygame.draw.rect(screen, GOLD, panel, 2, border_radius=6)
        centered(message, 598, font_small)


def draw_pause():
    draw_game()
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, (0, 0))
    centered("PAUSADO", 240, font_title, GOLD)
    resume_button.draw()
    menu_button.draw()


def draw_complete():
    screen.fill((7, 16, 18))
    completed_name = ERAS[level_id - 1]["name"].upper()
    centered(f"{completed_name} CONCLUIDO", 235, font_title, GOLD)
    centered("Fragmento temporal recuperado.", 340, font_body)
    if level_id < 5:
        next_name = ERAS[level_id]["name"].upper()
        next_text = f"{next_name} DESBLOQUEADA"
    else:
        next_text = "PROXIMAS EPOCAS EM DESENVOLVIMENTO"
    centered(next_text, 405, font_heading, CYAN)
    centered("ENTER continua para a proxima fase", 610, font_small, GRAY)


def update_camera():
    global camera_x
    target = player.rect.centerx - WIDTH * 0.4
    camera_x += (target - camera_x) * 0.1
    camera_x = max(0, min(camera_x, level.WIDTH - WIDTH))


def update_game():
    global message_timer, state
    player.update(pygame.key.get_pressed(), level.WIDTH)
    level.update()
    update_camera()
    if level.puzzle_solved and level.fragment.collect_if_near(player):
        campaign.complete_level(level_id)
        if level_id == 1:
            show_message("Fragmento temporal recuperado. Grecia Antiga desbloqueada.", 5)
        else:
            show_message("Fragmento da Grecia recuperado.", 5)
        state = COMPLETE
    if message_timer > 0:
        message_timer -= 1


def update_buttons():
    for button in (play_button, continue_button, era_button, settings_button, exit_button, resume_button, menu_button):
        button.update()


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if state == STORY and event.key == pygame.K_RETURN:
                if story.advance():
                    state = GAME
            elif state == GAME:
                if event.key == pygame.K_ESCAPE:
                    state = PAUSE
                elif event.key == pygame.K_e:
                    result = level.interact(player)
                    if result == "artifact":
                        show_message("O artefato abriu uma passagem para o Egito Antigo.", 4)
                    elif result == "puzzle":
                        show_message(level.message)
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    level.puzzle_key(event.key)
                    if level.message:
                        show_message(level.message)
            elif state == PAUSE and event.key == pygame.K_ESCAPE:
                state = GAME
            elif state == ERA_SELECT and event.key == pygame.K_ESCAPE:
                state = MENU
            elif state == ERA_SELECT and event.key in (
                pygame.K_2,
                pygame.K_3,
                pygame.K_4,
                pygame.K_5,
            ):
                selected_level = event.key - pygame.K_0
                start_level(selected_level)
            elif state == SETTINGS and event.key == pygame.K_ESCAPE:
                state = MENU
            elif state == COMPLETE and event.key == pygame.K_RETURN:
                if level_id < 5:
                    start_level(level_id + 1)
                else:
                    state = MENU
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == MENU:
                if play_button.rect.collidepoint(event.pos):
                    begin_story()
                elif continue_button.rect.collidepoint(event.pos):
                    begin_story()
                elif era_button.rect.collidepoint(event.pos):
                    state = ERA_SELECT
                elif settings_button.rect.collidepoint(event.pos):
                    state = SETTINGS
                elif exit_button.rect.collidepoint(event.pos):
                    running = False
            elif state == PAUSE:
                if resume_button.rect.collidepoint(event.pos):
                    state = GAME
                elif menu_button.rect.collidepoint(event.pos):
                    state = MENU

    if state in (MENU, PAUSE):
        update_buttons()
    elif state == GAME:
        update_game()

    if state == MENU:
        draw_menu()
    elif state == STORY:
        draw_story()
    elif state == ERA_SELECT:
        draw_eras()
    elif state == GAME:
        draw_game()
    elif state == PAUSE:
        draw_pause()
    elif state == SETTINGS:
        draw_settings()
    elif state == COMPLETE:
        draw_complete()
    pygame.display.flip()

pygame.quit()
sys.exit()
