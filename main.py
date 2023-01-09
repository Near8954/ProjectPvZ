import pygame
import os
import sys

size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


plants_images = {'sunflower': pygame.transform.scale(load_image('PvZ/1/sunflower.png'), (70, 70)),
                 'windflower': pygame.transform.scale(load_image('PvZ/2/windflower.png'), (70, 70)),
                 'peasflower': pygame.transform.scale(load_image('PvZ/3/peasflower.png'), (70, 70)),
                 'fireflower': [pygame.transform.scale(load_image('PvZ/4/fireflower_active.png'), (70, 70)),
                                pygame.transform.scale(load_image('PvZ/4/fireflower_inactive.png'), (70, 70))],
                 'cactus': pygame.transform.scale(load_image('PvZ/5/cactus.png'), (70, 70))}


class Board:
    # создание поля
    def __init__(self, width, height, left, top):
        self.width = width
        self.height = height
        self.board = [[0] * height for _ in range(width)]

        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = 70

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
        x, y = mouse_pos
        x -= self.left
        y -= self.top
        if (x <= 0 or y <= 0 or x >= self.width * self.cell_size
                or y >= self.height * self.cell_size):
            return None

        return x // self.cell_size, y // self.cell_size

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        return cell

    def plant(self, obj, coords):
        self.board[coords[0]][coords[1]] = obj

    def check_cell(self,x,y):
        if self.board[x][y]:
            return False
        return True


class ChoiceBoard(Board):
    def put_plants(self, plants):
        self.map = {(0, 0): plants[0], (1, 0): plants[1], (2, 0): plants[2], (3, 0): plants[3],
                    (4, 0): plants[4]}
        self.plants = {(0, 0): 'sunflower', (1, 0): 'windflower', (2, 0): 'peasflower', (3, 0): 'fireflower',
                       (4, 0): 'cactus'}

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255),
                                 ((self.left + x * self.cell_size,
                                   self.top + y * self.cell_size),
                                  (self.cell_size, self.cell_size)),
                                 True)
                screen.blit(self.map[(x, y)], (50 + x * 70, 20))

    def choose_plant(self, coords):
        self.current_plant = self.plants[coords]
        return self.current_plant


class Sunflower(pygame.sprite.Sprite):
    image = plants_images['sunflower']

    def __init__(self, x, y):
        super().__init__()
        self.image = Sunflower.image
        self.rect = self.image.get_rect()
        self.rect.x = 50 + x * 70
        self.rect.y = 200 + y * 70


class Windflower(pygame.sprite.Sprite):
    image = plants_images['windflower']

    def __init__(self, x, y):
        super().__init__()
        self.image = Windflower.image
        self.rect = self.image.get_rect()
        self.rect.x = 50 + x * 70
        self.rect.y = 200 + y * 70


class Peasflower(pygame.sprite.Sprite):
    image = plants_images['peasflower']

    def __init__(self, x, y):
        super().__init__()
        self.image = Peasflower.image
        self.rect = self.image.get_rect()
        self.rect.x = 50 + x * 70
        self.rect.y = 200 + y * 70


class Fireflower(pygame.sprite.Sprite):
    image_inactive = plants_images['fireflower'][1]
    image_active = plants_images['fireflower'][0]

    def __init__(self, x, y):
        super().__init__()
        self.image = Fireflower.image_inactive

        self.rect = self.image_inactive.get_rect()
        self.rect.x = 50 + x * 70
        self.rect.y = 200 + y * 70


class Cactus(pygame.sprite.Sprite):
    image = plants_images['cactus']

    def __init__(self, x, y):
        super().__init__()
        self.image = Cactus.image
        self.rect = self.image.get_rect()
        self.rect.x = 50 + x * 70
        self.rect.y = 200 + y * 70


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('temp_start_menu.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(FPS)


def plant(name, x, y,board):
    if board.check_cell(x,y):
        if name == 'sunflower':
            plant = Sunflower(x, y)
        elif name == 'windflower':
            plant = Windflower(x, y)
        elif name == 'peasflower':
            plant = Peasflower(x, y)
        elif name == 'fireflower':
            plant = Fireflower(x, y)
        elif name == 'cactus':
            plant = Cactus(x, y)
        board.board[x][y]=1
        all_sprites.add(plant)


def play():
    running = True
    fps = 60

    start_sunflower = Sunflower(0, 2)
    all_sprites.add(start_sunflower)
    clock = pygame.time.Clock()
    main_board = Board(10, 5, 50, 200)

    choice_board = ChoiceBoard(5, 1, 50, 20)
    choice_board.put_plants([plants_images['sunflower'], plants_images['windflower'], plants_images['peasflower'],
                             plants_images['fireflower'][0], plants_images['cactus']])
    background_grass = load_image('background_grass.png')
    screen.fill(pygame.Color('grey'))
    main_board.plant(start_sunflower, (0, 2))
    current_plant = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_board_click = main_board.get_click(event.pos)
                choice_board_click = choice_board.get_click(event.pos)
                if choice_board_click is not None:
                    current_plant = choice_board.choose_plant(choice_board_click)

                if main_board_click is not None and current_plant is not None:

                    plant(current_plant, main_board_click[0], main_board_click[1], main_board)

        screen.blit(background_grass, (50, 200))
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(fps)
        main_board.render(screen)
        choice_board.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('PvZ')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    start_screen()
    play()