import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('PvZ')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    running = True
    v = 5  # пикселей в секунду
    r = 0
    fps = 60
    is_circle = False
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(f'click:{x, y}')
        screen.fill((0, 0, 0))
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
