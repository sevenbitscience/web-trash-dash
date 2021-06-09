import pygame
import random


class Trash:
    def __init__(self):
        self.screenheight = 640
        self.trashSprites = [pygame.image.load("assets/gfx/appleCore.png"), pygame.image.load("assets/gfx/soda.png")]
        self.reset()

    def reset(self):
        self.size = random.randrange(20, 30)
        self.sprite = self.trashSprites[random.randint(0, len(self.trashSprites) - 1)]
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        self.sprite = pygame.transform.rotate(self.sprite, random.randrange(0, 360))
        self.position = [random.randrange(370, 1100), random.randrange(-300, -self.size)]
        self.speed = random.uniform(0.5, 1)

    def fall(self):
        if self.position[1] < self.screenheight:
            self.position[1] += self.speed
        else:
            self.reset()


class Player:
    def __init__(self):
        self.speed = 2
        self.position = [100, 400]
        self.velocity = [0, 0]
        self.idle = pygame.image.load("assets/gfx/dino.png")
        self.rightSprite = self.idle
        self.rightSprite = pygame.transform.scale(self.rightSprite, (60, 60))
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)
        self.currentSprite = self.rightSprite


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

    dino = Player()
    left = False

    # create trash pieces
    trash_pieces = []

    for i in range(20):
        trash_pieces.append(Trash())

    # bools for what menu to be in
    running = False
    shop_open = False

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

            if not shop_open:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_a]:
                    dino.velocity[0] = -dino.speed
                    if not left:
                        left = True
                        dino.currentSprite = dino.leftSprite
                if pressed[pygame.K_d]:
                    dino.velocity[0] = dino.speed
                    if left:
                        left = False
                        dino.currentSprite = dino.rightSprite
                if pressed[pygame.K_w]:
                    dino.velocity[1] = -dino.speed
                if pressed[pygame.K_s]:
                    dino.velocity[1] = dino.speed

                if not -0.5 > dino.velocity[0] > 0.5:
                    dino.position[0] += dino.velocity[0]
                    dino.velocity[0] = 0
                if not -0.5 > dino.velocity[1] > 0.5:
                    dino.position[1] += dino.velocity[1]
                    dino.velocity[1] = 0

                screen.blit(house, (0, 0))

                for trash in trash_pieces:
                    screen.blit(trash.sprite, (trash.position[0], trash.position[1]))
                    trash.fall()

                screen.blit(dino.currentSprite, dino.position)

            clock.tick(60)
            print(clock.get_fps())
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
