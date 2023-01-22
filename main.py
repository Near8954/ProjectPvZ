import pygame
import os
import sys
import random
import datetime as dt

size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
sunflowers = pygame.sprite.Group()
peasflowers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
plants = pygame.sprite.Group()
peases = pygame.sprite.Group()
sun = 40



def load_image(name, colorkey=None):  # загрузка изображений
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


plants_images = {'sunflower': [pygame.transform.scale(load_image('PvZ/1/sunflower.png'), (70, 70)),
                               pygame.transform.scale(load_image('PvZ/1/sunflower2.png'), (70, 70))],
                 'windflower': pygame.transform.scale(load_image('PvZ/2/windflower.png'), (70, 70)),
                 'peasflower': pygame.transform.scale(load_image('PvZ/3/peasflower.png'), (70, 70)),
                 'fireflower': [pygame.transform.scale(load_image('PvZ/4/fireflower_active.png'), (70, 70)),
                                pygame.transform.scale(load_image('PvZ/4/fireflower_inactive.png'), (70, 70))],
                 'cactus': pygame.transform.scale(load_image('PvZ/5/cactus.png'), (70, 70)),
                 'peas': pygame.transform.scale(load_image('PvZ/3/Sprite-0001.png'), (110, 110))}
# изображения всех растений
enemies_images = {'snail': [pygame.transform.scale(load_image('PvZ/enemy_1/snail1.png'), (70, 70)),
                            pygame.transform.scale(load_image('PvZ/enemy_1/snail2.png'), (70, 70))]}
# изображения врагов

class Board:
    # создание игрового поля
    def __init__(self, width, height, left, top):
        self.width = width
        self.height = height
        self.board = [[0] * height for _ in range(width)]
        global board

        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = 70
        self.price_of_plants = (10, 20, 30, 40, 50)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255),
                                 ((self.left + x * self.cell_size,
                                   self.top + y * self.cell_size),
                                  (self.cell_size, self.cell_size)),
                                 True)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos  # инструменты для определения нажатия
        x -= self.left
        y -= self.top
        if (x <= 0 or y <= 0 or x >= self.width * self.cell_size
                or y >= self.height * self.cell_size):
            return None

        return x // self.cell_size, y // self.cell_size

    def on_click(self, cell_coords):  # инструменты для определения нажатия
        print(cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)  # инструменты для определения нажатия
        return cell

    def plant(self, obj, coords):  # функция посадки растения
        self.board[coords[0]][coords[1]] = obj

    def check_cell(self, x, y):  # инструменты для определения нажатия
        if self.board[x][y]:
            return False
        return True
    
    def change(self, x, y):
        self.board[x][y] = 0


class ChoiceBoard(Board):  # поле выбора растений
    def put_plants(self, plants):  # два словаря - кто в каком поле сидит
        self.map = {(0, 0): plants[0], (1, 0): plants[1], (2, 0): plants[2], (3, 0): plants[3],
                    (4, 0): plants[4]}
        self.plants = {(0, 0): 'sunflower', (1, 0): 'windflower', (2, 0): 'peasflower', (3, 0): 'fireflower',
                       (4, 0): 'cactus'}

    def render(self, screen):
        font = pygame.font.Font(None, 40)  # вывод поля

        for y in range(self.height):
            for x in range(self.width):
                text = font.render(str(self.price_of_plants[x]), True, (0, 0, 0))
                pygame.draw.rect(screen, (255, 255, 255),
                                 ((self.left + x * self.cell_size,
                                   self.top + y * self.cell_size),
                                  (self.cell_size, self.cell_size + 25)),
                                 True)
                screen.blit(self.map[(x, y)], (50 + x * 70, 20))
                text_w = text.get_width()
                text_h = text.get_height()
                text_x = self.left + x * self.cell_size + (self.cell_size - text_w) // 2
                text_y = self.top + 70
                screen.blit(text, (text_x, text_y))

    def choose_plant(self, coords):  # выбор растения
        self.current_plant = self.plants[coords]
        return self.current_plant


class Sunflower(pygame.sprite.Sprite):
    image = plants_images['sunflower'][0]
    image2 = plants_images['sunflower'][1]

    def __init__(self, x, y):
        global sun
        sun -= 10
        self.hp = 100
        self.x = x
        self.y = y
        super().__init__()
        self.mask = pygame.mask.from_surface(self.image)
        self.mask2 = pygame.mask.from_surface(self.image2)
        self.born_time = dt.datetime.now()
        self.image = Sunflower.image
        self.rect = self.image.get_rect()
        self.rect.x = 50 + x * 70
        self.rect.y = 200 + y * 70
        self.get_sun = True

    def check_time_to_sun(self):
        global sun
        time_now = dt.datetime.now()

        delta = (time_now - self.born_time).seconds

        if delta % 5 == 0 and delta and self.get_sun:
            self.image = Sunflower.image2
            sun += 5
            self.get_sun = False
        elif delta % 5 == 1:
            self.image = Sunflower.image
            self.get_sun = True
    
    def update(self):
        for obj in enemies:
            if pygame.sprite.collide_mask(self, obj):
                self.hp -= 0.5
        if self.hp <= 0:
            self.kill()
            board.change(self.x, self.y)
        print(self.hp)

class Windflower(pygame.sprite.Sprite):
    image = plants_images['windflower']

    def __init__(self, x, y):
        global sun
        sun -= 20
        super().__init__()
        self.mask = pygame.mask.from_surface(self.image)
        self.image = Windflower.image
        self.rect = self.image.get_rect()
        self.rect.x = 50 + x * 70
        self.rect.y = 200 + y * 70
        self.hp = 100
    
    def update(self):
        for obj in enemies:
            if pygame.sprite.collide_mask(self, obj):
                self.hp -= 0.5
        if self.hp <= 0:
            self.kill()
        


class Peas(pygame.sprite.Sprite):
    image = plants_images['peas']

    def __init__(self, x, y):
        super().__init__()
        self.mask = pygame.mask.from_surface(self.image)
        self.image = Peas.image
        self.rect = self.image.get_rect()
        self.rect.x = 50 + x * 70 + 5
        self.rect.y = 160 + y * 70
        self.hp = 100

    def update(self):
        self.rect.x += 1
        if self.rect.x >= 800:
            self.kill()
        for obj in enemies:
            if pygame.sprite.collide_mask(self, obj):
                self.hp -= 0.5
        if self.hp <= 0:
            self.kill()
        


class Peasflower(pygame.sprite.Sprite):
    image = plants_images['peasflower']

    def __init__(self, x, y):
        global sun
        sun -= 30
        super().__init__()
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.born_time = dt.datetime.now()
        self.image = Peasflower.image
        self.rect = self.image.get_rect()
        self.rect.x = 50 + x * 70
        self.rect.y = 200 + y * 70
        self.shoot = True
        self.hp = 100

    def check_time_to_shoot(self):

        time_now = dt.datetime.now()

        delta = (time_now - self.born_time).seconds

        if delta % 5 == 0 and delta and self.shoot:

            peas = Peas(self.x, self.y)
            peases.add(peas)
            all_sprites.add(peas)
            self.shoot = False
        elif delta % 5 == 1:
            self.shoot = True
    
    def update(self):
        for obj in enemies:
            if pygame.sprite.collide_mask(self, obj):
                self.hp -= 0.5
        if self.hp <= 0:
            self.kill()


class Fireflower(pygame.sprite.Sprite):
    image_inactive = plants_images['fireflower'][1]
    image_active = plants_images['fireflower'][0]

    def __init__(self, x, y):
        global sun
        sun -= 40
        super().__init__()
        self.image = Fireflower.image_inactive
        self.mask = pygame.mask.from_surface(self.image_inactive)
        self.mask = pygame.mask.from_surface(self.image_active)
        self.rect = self.image_inactive.get_rect()
        self.rect.x = 50 + x * 70
        self.hp = 100
        self.rect.y = 200 + y * 70
    
    def update(self):
        for obj in enemies:
            if pygame.sprite.collide_mask(self, obj):
                self.hp -= 0.5
        if self.hp <= 0:
            self.kill()


class Cactus(pygame.sprite.Sprite):
    image = plants_images['cactus']

    def __init__(self, x, y):
        global sun
        sun -= 50
        super().__init__()
        self.mask = pygame.mask.from_surface(self.image)
        self.image = Cactus.image
        self.rect = self.image.get_rect()
        self.rect.x = 50 + x * 70
        self.rect.y = 200 + y * 70
        self.hp = 200
    
    def update(self):
        for obj in enemies:
            if pygame.sprite.collide_mask(self, obj):
                self.hp -= 0.5
        if self.hp <= 0:
            self.kill()


class Snail(pygame.sprite.Sprite):
    image_1 = enemies_images['snail'][0]
    image_2 = enemies_images['snail'][1]

    def __init__(self, x, y):
        super().__init__()
        self.image = Snail.image_1
        self.mask = pygame.mask.from_surface(self.image_1)
        self.mask2 = pygame.mask.from_surface(self.image_2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.speed = 1
        self.rect.y = 210 + y * 70

    def update(self):
        self.f = False
        for obj in plants:
            if pygame.sprite.collide_mask(self, obj):
                self.speed = 0
                self.f = True
        if not self.f:
            self.speed = 1
            self.f = False
        self.rect.x -= self.speed
        if self.rect.x == 0:
            self.kill()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    def text(screen):
        font = pygame.font.Font(None, 100)
        but_color = pygame.Color((102, 0, 102))
        intro_text = "ВРАГИ-ЖУКИ"
        text = font.render(intro_text, True, (255, 255, 255))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = (800 - text_w) // 2
        text_y = 70
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, but_color, (300, 200, 200, 50))

        font = pygame.font.Font(None, 40)
        text = font.render('СТАРТ', True, (255, 255, 255))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = (200 - text_w) // 2 + 300
        text_y = (50 - text_h) // 2 + 200
        screen.blit(text, (text_x, text_y))

        pygame.draw.rect(screen, but_color, (300, 300, 200, 50))
        font = pygame.font.Font(None, 40)
        text = font.render('УРОВНИ', True, (255, 255, 255))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = (200 - text_w) // 2 + 300
        text_y = (50 - text_h) // 2 + 300
        screen.blit(text, (text_x, text_y))

        pygame.draw.rect(screen, but_color, (300, 400, 200, 50))
        font = pygame.font.Font(None, 40)
        text = font.render('ОПИСАНИЕ', True, (255, 255, 255))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = (200 - text_w) // 2 + 300
        text_y = (50 - text_h) // 2 + 400
        screen.blit(text, (text_x, text_y))

    while True:

        screen.fill((119, 221, 119))
        text(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                if 300<=x and x<=500 and 200<=y and y<=250:
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def plant(name, x, y, board):  # функция посадки растения
    if board.check_cell(x, y):
        if name == 'sunflower' and sun >= 10:
            plant = Sunflower(x, y)
        elif name == 'windflower' and sun >= 20:
            plant = Windflower(x, y)
        elif name == 'peasflower' and sun >= 30:
            plant = Peasflower(x, y)
        elif name == 'fireflower' and sun >= 40:
            plant = Fireflower(x, y)
        elif name == 'cactus' and sun >= 50:
            plant = Cactus(x, y)
        else:
            plant = None
        if plant is not None:

            board.plant(plant, (x, y))
            all_sprites.add(plant)
            plants.add(plant)
            if name == 'sunflower':
                sunflowers.add(plant)
            elif name == 'peasflower':
                peasflowers.add(plant)


def random_spawn():
    name = random.choice(list(enemies_images.keys()))
    x, y = 780, random.randint(0, 4)
    if name == 'snail':
        enemy = Snail(x, y)
        all_sprites.add(enemy)
        enemies.add(enemy)


def show_sun():
    font = pygame.font.Font(None, 40)
    text = font.render(str(sun), True, (0, 0, 0))
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = 700
    text_y = 20
    screen.blit(text, (text_x, text_y))


def play():
    running = True
    fps = 60

    start_sunflower = Sunflower(0, 2)
    all_sprites.add(start_sunflower)
    sunflowers.add(start_sunflower)
    plants.add(start_sunflower)
    clock = pygame.time.Clock()
    main_board = Board(10, 5, 50, 200)

    choice_board = ChoiceBoard(5, 1, 50, 20)
    choice_board.put_plants([plants_images['sunflower'][0],
                             plants_images['windflower'],
                             plants_images['peasflower'],
                             plants_images['fireflower'][0],
                             plants_images['cactus']])

    background_grass = load_image('background_grass.png')

    main_board.plant(start_sunflower, (0, 2))
    current_plant = None  # растение которое хотим посадить (в начале - никакое)
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 10000)
    while running:
        screen.fill(pygame.Color('grey'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == MYEVENTTYPE:
                random_spawn()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_board_click = main_board.get_click(event.pos)
                # проверка что куда садим
                choice_board_click = choice_board.get_click(event.pos)

                if choice_board_click is not None:
                    current_plant = choice_board.choose_plant(choice_board_click)

                if main_board_click is not None and current_plant is not None:
                    plant(current_plant, main_board_click[0], main_board_click[1], main_board)

        screen.blit(background_grass, (50, 200))
        all_sprites.update()
        show_sun()
        for obj in sunflowers:
            obj.check_time_to_sun()
        for obj in peasflowers:
            obj.check_time_to_shoot()
        all_sprites.draw(screen)

        clock.tick(fps)
        main_board.render(screen)
        choice_board.render(screen)

        peases.draw(screen)
        enemies.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('PvZ')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    start_screen()
    play()
