import pygame
import random


class Trash:
    trashSprites = None

    def __init__(self):
        self.screenheight = 640
        if self.trashSprites is None:
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

    # load title_screen picture
    title_screen = pygame.image.load("assets/gfx/TitleScreen.png")
    title_screen = pygame.transform.scale(title_screen, (1280, 640))

    # load outside picture
    house = pygame.image.load("assets/gfx/house.png")
    house = pygame.transform.scale(house, (1280, 640))

    # Load assets for the atm
    atm = pygame.image.load("assets/gfx/atm.png")
    atm = pygame.transform.scale(atm, (1280, 640))
    shop_hitbox = (100, 230, 70, 70)
    sell_font = pygame.font.SysFont("calibri", 40)
    sell_text = sell_font.render("Sell", True, (235, 235, 235))
    sell_button_color = (71, 145, 64)
    sell_button = (383, 445, 542, 80)
    sell_rect = pygame.Rect(sell_button)

    # load stuff for hotbar
    score_font = pygame.font.SysFont("calibri", 50)
    score_color = (191, 69, 69)
    hud_icon_size = 60
    trash_pile = pygame.image.load("assets/gfx/soda.png")
    trash_pile = pygame.transform.scale(trash_pile, (hud_icon_size, hud_icon_size))
    coin = pygame.image.load("assets/gfx/coin.png")
    coin = pygame.transform.scale(coin, (hud_icon_size, hud_icon_size))
    timer_icon = pygame.image.load("assets/gfx/hourglass-icon.png")
    timer_icon = pygame.transform.scale(timer_icon, (hud_icon_size, hud_icon_size))
    backpack_icon = pygame.image.load("assets/gfx/backpack-icon.png")
    backpack_icon = pygame.transform.scale(backpack_icon, (hud_icon_size, hud_icon_size))
    trash_text = score_font.render(str(0), True, score_color)
    score_text = score_font.render(str(0), True, score_color)
    backpack_text = score_font.render(str(10), True, score_color)
    score_holder = pygame.Rect(10, 550, 600, 80)

    barriers = [(0, 0, 280, 200), (80, 200, 70, 70)]

    upgrades_font = pygame.font.SysFont("calibri", 18)
    upgrade_text_color = (36, 36, 36)
    start_button = (985, 435, 205, 90)
    start_text = upgrades_font.render("Next day", True, upgrade_text_color)
    quit_button = (985, 320, 205, 90)
    quit_text = upgrades_font.render("Quit", True, (181, 23, 2))
    inside = pygame.image.load("assets/gfx/inside.png")
    inside = pygame.transform.scale(inside, (1280, 640))

    start_ticks = pygame.time.get_ticks()
    last_seconds = -1
    total_time = 60
    time_left = total_time
    timer_width = 490
    timer_step = timer_width / time_left
    timer_rect = [650, 562, timer_width, 55]
    timer_color = [0, 255, 0]

    dino = Player()
    keys = {
        'up': False,
        'down': False,
        'left': False,
        'right': False
    }

    trash_collected = 0
    balance = 0
    trash_price = 0
    backpack = 10

    # create trash pieces
    trash_pieces = []

    for i in range(15):
        trash_pieces.append(Trash())

    # bools for what menu to be in
    running = True
    shop_open = False
    selling = False
    interact = False
    select = False

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
            interact = False
            select = False

            current_ticks = pygame.time.get_ticks()
            seconds = int(((current_ticks - start_ticks) / 1000))
            if last_seconds != seconds:
                time_left -= seconds - last_seconds
                # print(time_left)
                last_seconds = seconds
                timer_rect[2] = timer_width - (timer_step * (total_time - time_left))

            if time_left >= 30:
                timer_color = [103, 219, 53]
            elif 15 < time_left < 30:
                timer_color = [245, 197, 39]
            elif 0 < time_left < 15:
                timer_color = [184, 44, 22]
            elif time_left <= 0:
                running = False

            for event in pygame.event.get():
                # find which keys are pressed
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    select = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        interact = True
                    if event.key == pygame.K_LEFT:
                        keys["left"] = True
                    if event.key == pygame.K_RIGHT:
                        keys["right"] = True
                    if event.key == pygame.K_UP:
                        keys["up"] = True
                    if event.key == pygame.K_DOWN:
                        keys["down"] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        keys["left"] = False
                    if event.key == pygame.K_RIGHT:
                        keys["right"] = False
                    if event.key == pygame.K_UP:
                        keys["up"] = False
                    if event.key == pygame.K_DOWN:
                        keys["down"] = False

            if not shop_open:

                if True in keys.values():
                    # Use which keys are being pressed to find which way to move
                    if keys["left"]:
                        dino.velocity[0] = -dino.speed
                        dino.currentSprite = dino.leftSprite
                    if keys["right"]:
                        dino.velocity[0] = dino.speed
                        dino.currentSprite = dino.rightSprite
                    if keys["up"]:
                        dino.velocity[1] = -dino.speed
                    if keys["down"]:
                        dino.velocity[1] = dino.speed

                    # if keys in opposite directions are pressed
                    if keys["left"] and keys["right"]:
                        dino.velocity[0] = 0
                    if keys["up"] and keys["down"]:
                        dino.velocity[1] = 0

                    # find the next position of the dino
                    next_pos = [(dino.position[0] + 8) + dino.velocity[0], (dino.position[1] + 6) + dino.velocity[1],
                                45, 52]

                    # deal with x positions:
                    # check if the dino is going to be within the screen
                    if dino.velocity[0] != 0:

                        for barrier in barriers:
                            if check_collision_list(next_pos, barrier):
                                dino.velocity[0] = 0

                        # if the dino needs to move, move it
                        if 0 < next_pos[0] < screen.get_width() - next_pos[2]:
                            dino.position[0] += dino.velocity[0]
                            dino.velocity[0] = 0

                    # deal with y positions
                    # check if the dino is going to be within the screen
                    if dino.velocity[1] != 0:

                        for barrier in barriers:
                            if check_collision_list(next_pos, barrier):
                                dino.velocity[1] = 0

                        # if the dino needs to move, move it
                        if 0 < next_pos[1] < 490:
                            dino.position[1] += dino.velocity[1]
                            dino.velocity[1] = 0

                if interact and check_collision_list([dino.position[0], dino.position[1], 45, 52], shop_hitbox):
                    shop_open = True
                    selling = False

                screen.blit(house, (0, 0))

                for trash in trash_pieces:

                    if interact and trash_collected < backpack:
                        if check_collision_list([dino.position[0], dino.position[1], 45, 52],
                                                [trash.position[0], trash.position[1], trash.size, trash.size]):
                            trash_collected += 1
                            trash_text = score_font.render(str(trash_collected), True, score_color)
                            trash.__init__()
                    screen.blit(trash.sprite, (trash.position[0], trash.position[1]))
                    trash.fall()

                screen.blit(dino.currentSprite, dino.position)

                pygame.draw.rect(screen, (38, 24, 24), score_holder, 0, 10)
                screen.blit(trash_pile, (20, 560))
                screen.blit(trash_text, (80, 567))
                screen.blit(coin, (200, 560))
                screen.blit(score_text, (270, 567))
                screen.blit(backpack_icon, (450, 560))
                screen.blit(backpack_text, (510, 567))

                pygame.draw.rect(screen, (38, 24, 24), (640, 550, 560, 80), 0, 10)
                screen.blit(timer_icon, (1130, 560))
                pygame.draw.rect(screen, timer_color, timer_rect, 0, 10)

            if shop_open:

                if select and not selling:
                    mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 3, 3)
                    if check_collision_list(mouse_pos, sell_button):
                        if trash_collected > 0:
                            start_sell = pygame.time.get_ticks()
                            selling = True
                        else:
                            shop_open = False

                if selling:
                    current_sell = pygame.time.get_ticks()
                    time_elapsed = current_sell - start_sell
                    if time_elapsed >= 5000:
                        balance += trash_collected * trash_price
                        trash_collected = 0
                        trash_text = score_font.render(str(trash_collected), True, score_color)
                        score_text = score_font.render(str(balance), True, score_color)
                        selling = False
                        shop_open = False

                # Update screen
                screen.blit(atm, [0, 0])
                if selling:
                    pygame.draw.rect(screen, (50, 50, 50), sell_rect, 0, 10)
                    pygame.draw.rect(screen, sell_button_color, (sell_rect[0], sell_rect[1],
                                                                 sell_rect[2] - int(time_elapsed / 9.2)
                                                                 , sell_rect[3]), 0, 10)
                else:
                    pygame.draw.rect(screen, sell_button_color, sell_rect, 0, 10)

                screen.blit(sell_text, (570, 465))
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
