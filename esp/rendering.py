import pygame
import time

def render_esp():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Hintergrund

        # ESP-Rechtecke für Feinde
        enemies = [(300, 200), (400, 300), (500, 400)]  # Beispiel-Positionen für Feinde
        for enemy in enemies:
            pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1], 50, 100), 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
