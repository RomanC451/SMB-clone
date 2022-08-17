from typing import Callable
from .physic_component import PhysicComponent

# from items.items_group import ItemsGroup
from enemies.enemies_group import EnemiesGroup


class TileBumpingAnimation:
    def __init__(self, physic_component: PhysicComponent, end_animation_handler: Callable) -> None:
        self.starting_y_tile_coord = physic_component.rect.x
        self.physic_component = physic_component
        self.end_animation_handler = end_animation_handler

        self.start_animation()

    def start_animation(self):

        self.physic_component.jump()

    def update(self, enemies_group: EnemiesGroup) -> None:
        self.physic_component.move_vertical_axis()
        self.check_collision(enemies_group)
        self.physic_component.move_horizontal_axis()
        self.physic_component.jump()

    def check_collision(self, enemies_group: EnemiesGroup) -> None:
        # colliding_items = items_group.get_colliding_items(self.physic_component.rect)
        # for item in colliding_items:
        #     item.under_tile_hit()

        colliding_enemies = enemies_group.get_colliding_enemies(self.physic_component.rect)
        for enemy in colliding_enemies:
            enemy.under_tile_hit()

    def check_animation_ending(self) -> None:
        if self.physic_component.rect.top >= self.starting_y_tile_coord:
            self.physic_component.reset_velocities()
            self.physic_component.rect.top = self.starting_y_tile_coord
            self.end_animation_handler()
