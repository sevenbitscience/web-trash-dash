import pygame
import random


class Trash:
    def __init__(self):
        self.trashSprite = pygame.image.load("assets/gfx/appleCore.png")
        self.sprite = self.TrashSprite
        self.position = pygame.Vector2(200, 200)


def check_collision_list(a, b):
    return (a[0] + a[2] > b[0]) and (a[0] < b[0] + b[2]) and (a[1] + a[3] > b[1]) and (a[1] < b[1] + b[3])


def main():
    # start pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 640))
    # pygame.display.set_caption("Trash dash")

    title_screen = pygame.image.load("assets/gfx/TitleScreen.png")
    title_screen = pygame.transform.scale(title_screen, (1280, 640))

    house = pygame.image.load("assets/gfx/house.png")
    house = pygame.transform.scale(house, (1280, 640))

    upgrades_font = pygame.font.Font("assets/Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 18)
    upgrade_text_color = (36, 36, 36)
    start_button = (985, 435, 205, 90)
    start_text = upgrades_font.render("Next day", True, upgrade_text_color)
    quit_button = (985, 320, 205, 90)
    quit_text = upgrades_font.render("Quit", True, (181, 23, 2))
    inside = pygame.image.load("assets/gfx/inside.png")
    inside = pygame.transform.scale(inside, (1280, 640))

    trash_pieces = Trash()

    running = False

    begin_button = (328, 191, 746, 72)
    screen.blit(title_screen, (0, 0))
    # pygame.draw.rect(screen, (0, 0, 0), begin_button)
    pygame.display.update()
    on_title = True

    while on_title:
        clock.tick(8)
        select = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                select = True
        if select:
            mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 3, 3)
            if check_collision_list(mouse_pos, begin_button):
                on_title = False

    while True:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            screen.blit(house, (0, 0))
            clock.tick(60)
            pygame.display.update()
        while not running:
            select = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    select = True
            if select:
                mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 3, 3)
                if check_collision_list(mouse_pos, start_button):
                    running = True
                elif check_collision_list(mouse_pos, quit_button):
                    return

            screen.blit(inside, (0, 0))
            screen.blit(quit_text, (1050, 363))
            screen.blit(start_text, (1010, 474))
            clock.tick(10)
            pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
