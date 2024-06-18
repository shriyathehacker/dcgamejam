import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

