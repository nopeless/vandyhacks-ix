import pygame


def pygame_event_to_dxdy(e):
    """
    Returns None if the key pressed is not relevant
    """
    if e.type != pygame.KEYDOWN:
        return
    return {
        pygame.K_w: (0, -1),
        pygame.K_UP: (0, -1),
        pygame.K_a: (-1, 0),
        pygame.K_LEFT: (-1, 0),
        pygame.K_s: (0, 1),
        pygame.K_DOWN: (0, 1),
        pygame.K_d: (1, 0),
        pygame.K_RIGHT: (1, 0),
    }.get(e.key, None)


def pygame_keys_x_axis(keys):
    x = 0
    if keys[pygame.K_a]:
        x -= 1
    if keys[pygame.K_d]:
        x += 1
    return x


def pygame_keys_y_axis(keys):
    y = 0
    if keys[pygame.K_s]:
        y -= 1
    if keys[pygame.K_w]:
        y += 1
    return y


def pygame_event_to_direction_index(e):
    """
    0: none
    1: up
    2: down
    3: left
    4: right
    """
    if e.type != pygame.KEYDOWN:
        return 0
    return {
        pygame.K_w: 1,
        pygame.K_UP: 1,
        pygame.K_a: 3,
        pygame.K_LEFT: 3,
        pygame.K_s: 2,
        pygame.K_DOWN: 2,
        pygame.K_d: 4,
        pygame.K_RIGHT: 4,
    }.get(e.key, 0)


def is_select(event):
    """
    Returns True if the key is select
    """
    return event.type == pygame.KEYDOWN and (
        event.key == pygame.K_RETURN or event.key == pygame.K_SPACE
    )


def is_restart(e):
    """
    Returns True if the key is restart
    """
    return e.type == pygame.KEYDOWN and e.key == pygame.K_r
