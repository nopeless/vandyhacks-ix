import pygame

"""
Accepts a world and modifies it
"""


def is_entity_colliding(entity, objects):
    return pygame.sprite.spritecollideany(
        entity, objects, collided=pygame.sprite.collide_mask
    )


def process_collision(movable_entity, static_entities):
    """
    This took more than 3 hours to write, but it works and don't touch it
    """
    if is_entity_colliding(movable_entity, static_entities):
        ox, oy = movable_entity.rect.x, movable_entity.rect.y
        dx = 0
        dy = 0
        for i in range(64):
            movable_entity.rect.x = ox + i
            if not is_entity_colliding(movable_entity, static_entities):
                dx = i
                break
            movable_entity.rect.x = ox - i
            if not is_entity_colliding(movable_entity, static_entities):
                dx = -i
                break

        # Reset movable_entity rect
        movable_entity.rect.x, movable_entity.rect.y = ox, oy

        for i in range(64):
            movable_entity.rect.y = oy + i
            if not is_entity_colliding(movable_entity, static_entities):
                dy = i
                break
            movable_entity.rect.y = oy - i
            if not is_entity_colliding(movable_entity, static_entities):
                dy = -i
                break

        # Reset movable_entity rect
        movable_entity.rect.x, movable_entity.rect.y = ox, oy

        angle = get_angle_from_xy(dx, dy)

        v = None

        # Circle quadrant calculations
        if dx < 0 and dy < 0:
            v = pygame.Vector2(-dy, -dx)
        if dx > 0 and dy < 0:
            v = pygame.Vector2(dy, dx)
        if dx > 0 and dy > 0:
            v = pygame.Vector2(-dy, -dx)
        if dx < 0 and dy > 0:
            v = pygame.Vector2(dy, dx)

        if dx == 0:
            v = pygame.Vector2(0, -dy)
        if dy == 0:
            v = pygame.Vector2(-dx, 0)

        if v.length() > 2:
            v = v.normalize()

            velocity_vector = pygame.Vector2(movable_entity.vx, movable_entity.vy)

            if abs(velocity_vector.angle_to(v)) < 90:
                velocity_vector = v.rotate(90) * velocity_vector.dot(v.rotate(90))

                movable_entity.vx = velocity_vector.x
                movable_entity.vy = velocity_vector.y

            movable_entity.rect.x += dx / 2
            movable_entity.rect.y += dy / 2


class Engine:
    def __init__(self, world):
        self.world = world

    def event(self, event):
        """
        Process pygame events
        """

    def update(self):
        """
        Updates itself based on 60hz
        """
