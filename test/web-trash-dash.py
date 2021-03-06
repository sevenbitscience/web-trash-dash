import pygame
import random


class Trash:
    trashSprites = None

    def __init__(self):
        self.screenheight = 640
        if self.trashSprites is None:
            self.trashSprites = [pygame.image.load("assets/gfx/appleCore.png"),
                                 pygame.image.load("assets/gfx/soda.png")]
        self.size = None
        self.sprite = None
        self.position = None
        self.speed = None
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
        self.frame = 0
        self.costume = 0

        self.walk = [pygame.image.load("assets/gfx/walking/DinoR1.png"),
                     pygame.image.load("assets/gfx/walking/DinoR2.png"),
                     pygame.image.load("assets/gfx/walking/DinoR3.png"),
                     pygame.image.load("assets/gfx/walking/DinoR4.png"),
                     pygame.image.load("assets/gfx/walking/DinoR5.png"),
                     pygame.image.load("assets/gfx/walking/DinoR6.png")]

        self.idle = pygame.image.load("assets/gfx/dino.png")

        self.duck_walk = [pygame.image.load("assets/gfx/DuckDino/DuckR1.png"),
                          pygame.image.load("assets/gfx/DuckDino/DuckR2.png"),
                          pygame.image.load("assets/gfx/DuckDino/DuckR3.png"),
                          pygame.image.load("assets/gfx/DuckDino/DuckR4.png"),
                          pygame.image.load("assets/gfx/DuckDino/DuckR5.png"),
                          pygame.image.load("assets/gfx/DuckDino/DuckR6.png")]

        self.duck_idle = pygame.image.load("assets/gfx/DuckDino/DuckIdle.png")

        self.robo_walk = [pygame.image.load("assets/gfx/RoboDino/ROBOR1.png"),
                          pygame.image.load("assets/gfx/RoboDino/ROBOR2.png"),
                          pygame.image.load("assets/gfx/RoboDino/ROBOR3.png"),
                          pygame.image.load("assets/gfx/RoboDino/ROBOR4.png"),
                          pygame.image.load("assets/gfx/RoboDino/ROBOR5.png"),
                          pygame.image.load("assets/gfx/RoboDino/ROBOR6.png")]

        self.robo_idle = pygame.image.load("assets/gfx/RoboDino/DinoBotIdle.png")

        self.rightSprite = self.idle
        self.rightSprite = pygame.transform.scale(self.rightSprite, (60, 60))
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)

    def animate(self, left):
        if self.frame >= len(self.walk):
            self.frame = 0

        if self.costume == 0:
            self.rightSprite = self.walk[self.frame]
        if self.costume == 1:
            self.rightSprite = self.robo_walk[self.frame]
        elif self.costume == 2:
            self.rightSprite = self.duck_walk[self.frame]

        self.rightSprite = pygame.transform.scale(self.rightSprite, (60, 60))
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)
        self.frame += 1

    def reset(self):
        if self.costume == 0:
            self.rightSprite = self.idle
        if self.costume == 1:
            self.rightSprite = self.robo_idle
        elif self.costume == 2:
            self.rightSprite = self.duck_idle

        self.rightSprite = pygame.transform.scale(self.rightSprite, (60, 60))
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)


def check_collision_list(a, b):
    return (a[0] + a[2] > b[0]) and (a[0] < b[0] + b[2]) and (a[1] + a[3] > b[1]) and (a[1] < b[1] + b[3])


def main():
    # start pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 640))

    # load title_screen picture
    title_screen = pygame.image.load("assets/gfx/TitleScreen.png")
    title_screen = pygame.transform.scale(title_screen, (1280, 640))

    screen.blit(title_screen, (0, 0))
    pygame.display.update()

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
    sell_rect = (383, 445, 542, 80)
    start_sell = 0
    time_elapsed = 0

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
    start_text = upgrades_font.render("Start day", True, upgrade_text_color)
    quit_button = (985, 320, 205, 90)
    quit_text = upgrades_font.render("Quit", True, (181, 23, 2))
    inside = pygame.image.load("assets/gfx/inside.png")
    inside = pygame.transform.scale(inside, (1280, 640))
    winScreen = pygame.image.load("assets/gfx/WinScreen.png")
    winScreen = pygame.transform.scale(winScreen, (1280, 640))
    GameWon = False
    winButton = (825, 255, 100, 55)
    backpack_button = (435, 255, 100, 55)
    speed_button = (570, 255, 100, 55)
    atm_button = (700, 255, 100, 55)
    selected_icon = (94, 71, 13, 13)
    costume_text = upgrades_font.render("Free", True, upgrade_text_color)
    costume1 = (72, 263, 71, 38)
    costume2 = (185, 263, 71, 38)
    costume3 = (299, 263, 71, 38)

    fact_font = pygame.font.SysFont("calibri", 12)
    facts = ("The Mississippi River carries an estimated 1.5 million metric tons of nitrogen pollution into the Gulf of Mexico each year, creating a dead zone in the Gulf each summer about the size of New Jersey.",
             "Approximately 40% of the lakes in America are too polluted for fishing, aquatic life, or swimming.",
             "Each year 1.2 trillion gallons of untreated sewage, stormwater, and industrial waste are dumped into US water.",
             "Every day, 2 million tons of sewage and industrial and agricultural waste are discharged into the world's water (UN WWAP 2003), the equivalent of the weight of the entire human population of 6.8 billion people.",
             "In developing countries, 70 percent of industrial wastes are dumped untreated into waters, polluting the usable water supply.",
             "More than 80% of sewage in developing countries is discharged untreated, polluting rivers, lakes, and coastal areas.",
             "About 10% of America's beaches fail to meet the federal benchmark for what constitutes safe swimming water.",
             "Federal authorities estimate that the headwaters of 40 percent of Western rivers are tainted with toxic discharge from abandoned mines.",
             "In the United States, there are thought to be over 20,000 known abandoned and uncontrolled hazardous waste sites, and these sites could contaminate the groundwater if there is a leak.",
             "The annual discharge of sewage and industrial waste in the Yangtze River has reached about 25 billion tons.",
             "More than 70 percent of China's rivers and lakes are polluted, government reports have said, and almost half may contain water unfit for human consumption or contact.",
             "Every year, more people die from unsafe water than from all forms of violence, including war.",
             "Industry dumps an estimated 300-400 MT of polluted waste in waters every year.",
             "Nitrate from agriculture is the most common chemical contaminant in the world's groundwater aquifers.",
             "Fresh water on earth is only 2.5% of the total water when 70% of the earth's surface is covered by water.",
             "Around 70% of industrial waste is dumped into the water.",
             "80% of the water pollution is caused due to domestic sewage.",
             "More than 6 billion pounds of garbage, mainly plastic, end up in the oceans every year.",
             "Contaminated water is the leading cause of various diseases such as cholera and typhus.",
             "Fifteen million children under five years die every year from diseases caused by drinking contaminated water.",
             "On average, 250 million people succumb each year to diseases caused by contaminated water. In contrast, according to the World Health Organization and UNICEF, almost 2.5 billion people lack access to valuable health conditions.",
             "The nuclear crisis created by the tsunami of 2011 unleashed 11 million liters of radioactive water into the Pacific Ocean.",
             "The same tsunami debris created islands totaling 70 kilometers in length which float in the ocean.",
             "Asia has the highest number of contaminated rivers than any other continent, the main bacteria from human waste.",
             "The Ganges river in India is considered the most polluted river globally and contains dirt, garbage, dead animals, and humans.",
             "Almost two million tons of human waste are exposed daily to water.",
             "Underground Bangladeshi water is contaminated with arsenic, which is highly toxic, poisonous, and carcinogenic.",
             "20% of groundwater in China, which is used as drinking water, is contaminated with carcinogens.",
             "In America, 40% of rivers and 46% of lakes are polluted and unsuitable for swimming, fishing, or any other activity.",
             "Water pollution kills around 10,000 people around the world every day - that is 3.6 million people every year;",
             "Every eight seconds, a child under the age of five dies from diseases related to contaminated water;",
             "Eighty percent of ocean pollution comes from land-based sources - oil, pesticides, septic tanks, dirt, discharge of nutrients, untreated sewage, run-off, farms, motor vehicles, ranches, etc.",
             "40 percent of China's water bodies are polluted, and roughly 700 million Chinese citizens drink contaminated water regularly;",
             "Oil is more harmful to the ocean's ecosystem than waste and trash;",
             "For every one million tons of oil that are shipped, one ton is spilled into the waterways;",
             "1.3 million gallons of oil is spilled into the ocean every year;",
             "Only 12 percent of the oil that is leaked into the ocean is the result of spills - the rest comes from land;")
    fact = facts[random.randrange(len(facts))]

    start_ticks = pygame.time.get_ticks()
    last_seconds = -1
    total_time = 10
    time_left = total_time
    timer_width = 490
    timer_step = timer_width / time_left
    timer_rect = [650, 562, timer_width, 55]
    timer_color = [0, 255, 0]

    dino = Player()
    last_frame = start_ticks
    left = False

    keys = {
        'up': False,
        'down': False,
        'left': False,
        'right': False
    }

    trash_collected = 0
    balance = 0
    trash_price = 5
    backpack = 10

    # create trash pieces
    trash_pieces = []

    for i in range(15):
        trash_pieces.append(Trash())

    # bools for what menu to be in
    running = False
    shop_open = False
    selling = False

    def box_text(surface, font, x_start, x_end, y_start, text, colour):
        x = x_start
        y = y_start
        words = text.split(' ')

        for word in words:
            word_t = font.render(word+' ', True, colour)
            if word_t.get_width() + x <= x_end:
                surface.blit(word_t, (x, y))
                x += word_t.get_width() + 2
            else:
                y += word_t.get_height() + 4
                x = x_start
                surface.blit(word_t, (x, y))
                x += word_t.get_width() + 2

    begin_button = (328, 191, 746, 72)
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
            elif time_left <= 0 and not shop_open:
                fact = facts[random.randrange(len(facts))]
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
                        dino.reset()
                    if event.key == pygame.K_RIGHT:
                        keys["right"] = False
                        dino.reset()
                    if event.key == pygame.K_UP:
                        keys["up"] = False
                        dino.reset()
                    if event.key == pygame.K_DOWN:
                        keys["down"] = False
                        dino.reset()

            if not shop_open:

                if True in keys.values():
                    # Use which keys are being pressed to find which way to move
                    if keys["left"]:
                        dino.velocity[0] = -dino.speed
                    if keys["right"]:
                        dino.velocity[0] = dino.speed
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

                    if dino.velocity[0] > 0:
                        left = False
                    elif dino.velocity[0] < 0:
                        left = True

                    if current_ticks - last_frame >= 80:
                        dino.animate(left)
                        last_frame = current_ticks

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
                            trash.reset()
                    screen.blit(trash.sprite, (trash.position[0], trash.position[1]))
                    trash.fall()

                if left:
                    screen.blit(dino.leftSprite, dino.position)
                else:
                    screen.blit(dino.rightSprite, dino.position)

                pygame.draw.rect(screen, (38, 24, 24), score_holder, 0, 10)
                screen.blit(trash_pile, (20, 560))
                screen.blit(trash_text, (80, 560))
                screen.blit(coin, (200, 560))
                screen.blit(score_text, (270, 560))
                screen.blit(backpack_icon, (450, 560))
                screen.blit(backpack_text, (510, 560))

                pygame.draw.rect(screen, (38, 24, 24), (640, 550, 560, 80), 0, 10)
                screen.blit(timer_icon, (1130, 560))
                pygame.draw.rect(screen, timer_color, timer_rect, 0, 10)

            if shop_open:

                if select and not selling:
                    mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 3, 3)
                    if check_collision_list(mouse_pos, sell_rect):
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
                        keys = {
                            'up': False,
                            'down': False,
                            'left': False,
                            'right': False
                        }

                # Update screen
                screen.blit(atm, [0, 0])
                if selling:
                    pygame.draw.rect(screen, (50, 50, 50), sell_rect, 0, 10)
                    pygame.draw.rect(screen, sell_button_color, (sell_rect[0], sell_rect[1],
                                                                 sell_rect[2] - int(time_elapsed / 9.2),
                                                                 sell_rect[3]), 0, 10)
                else:
                    pygame.draw.rect(screen, sell_button_color, sell_rect, 0, 10)

                screen.blit(sell_text, (600, 460))
            clock.tick(60)
            pygame.display.update()

        if trash_collected > 0:

            selling = True
            start_sell = pygame.time.get_ticks()

            while selling:
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
                                                                 sell_rect[2] - int(time_elapsed / 9.2),
                                                                 sell_rect[3]), 0, 10)
                else:
                    pygame.draw.rect(screen, sell_button_color, sell_rect, 0, 10)
                    screen.blit(sell_text, (600, 460))

                clock.tick(60)
                pygame.display.update()

        while not running and not selling:
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
                elif check_collision_list(mouse_pos, speed_button):
                    if dino.speed < 10 and balance >= dino.speed * 20:
                        balance -= dino.speed * 20
                        dino.speed += 1
                        score_text = score_font.render(str(balance), True, score_color)
                elif check_collision_list(mouse_pos, backpack_button):
                    if balance >= backpack * 3:
                        balance -= backpack * 3
                        backpack += 5
                        score_text = score_font.render(str(balance), True, score_color)
                        backpack_text = score_font.render(str(backpack), True, score_color)
                elif check_collision_list(mouse_pos, atm_button):
                    if balance >= trash_price * 10:
                        balance -= trash_price * 10
                        trash_price += 2
                        score_text = score_font.render(str(balance), True, score_color)
                elif check_collision_list(mouse_pos, costume1):
                    selected_icon = (94, 71, 13, 13)
                    dino.costume = 0
                    dino.reset()
                elif check_collision_list(mouse_pos, costume2):
                    selected_icon = (215, 71, 13, 13)
                    dino.costume = 1
                    dino.reset()
                elif check_collision_list(mouse_pos, costume3):
                    selected_icon = (329, 71, 13, 13)
                    dino.costume = 2
                    dino.reset()
                elif check_collision_list(mouse_pos, winButton):
                    if GameWon or balance >= 1000:
                        GameWon = True
                        pygame.time.delay(10)
                        screen.blit(winScreen, (0, 0))
                        pygame.display.update()
                        pygame.time.delay(50)
                        if not GameWon:
                            balance -= 1000

            screen.blit(inside, (0, 0))
            screen.blit(quit_text, (1070, 360))
            screen.blit(start_text, (1053, 468))

            pygame.draw.rect(screen, (13, 219, 67), selected_icon)
            screen.blit(costume_text, (90, 270))
            screen.blit(costume_text, (205, 270))
            screen.blit(costume_text, (315, 270))

            # pygame.draw.rect(screen, (13, 219, 67), backpack_button, 0, 20)
            screen.blit(upgrades_font.render(str(backpack * 3), True, score_color), (470, 270))

            # pygame.draw.rect(screen, (13, 219, 67), speed_button, 0, 20)
            screen.blit(upgrades_font.render(str((dino.speed * 20)), True, score_color), (608, 270))

            # pygame.draw.rect(screen, (13, 219, 67), atm_button, 0, 20)
            screen.blit(upgrades_font.render(str((trash_price * 10)), True, score_color), (735, 270))

            # pygame.draw.rect(screen, (13, 219, 67), winButton)
            if not GameWon:
                screen.blit(upgrades_font.render(str(1000), True, score_color), (862, 270))

            box_text(screen, fact_font, 1000, 1182, 85, fact, score_color)

            pygame.draw.rect(screen, (38, 24, 24), score_holder, 0, 10)
            screen.blit(trash_pile, (20, 560))
            screen.blit(trash_text, (80, 560))
            screen.blit(coin, (200, 560))
            screen.blit(score_text, (270, 560))
            screen.blit(backpack_icon, (450, 560))
            screen.blit(backpack_text, (510, 560))

            clock.tick(10)
            pygame.display.update()

        start_ticks = pygame.time.get_ticks()
        last_seconds = -1
        total_time = 60
        time_left = total_time
        timer_width = 490
        timer_step = timer_width / time_left
        timer_rect = [650, 562, timer_width, 55]
        last_frame = 0
        timer_width = 490
        dino.position = [100, 400]
        for trash in trash_pieces:
            trash.reset()

        keys = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        dino.reset()


if __name__ == "__main__":
    main()
    pygame.quit()
