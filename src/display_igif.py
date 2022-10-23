file = input("resource to evaluate ex) images.player_walking_test\n>")
import resources
import lib
import config
import pygame

image = resources

for i in file.split("."):
    image = image.__getattribute__(i)

size = (700, 500)

screen = config.screen

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))

    frame = image.frame
    screen.blit(
        pygame.transform.scale(frame, pygame.Vector2(frame.get_size()) * 10), (0, 0)
    )

    pygame.display.update()
    clock.tick(60)

# Close the window and quit.
pygame.quit()
