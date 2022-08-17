def sort_enemies_list(enemy1, enemy2):
    """Sort function of two enemies.

    Args:
        enemy1 (enemy):
        enemy2 (enemy):

    Returns:
        -1: if enemy1 is further to the left and lower than enemy2
        1: if enemy2 is further to the left and lower than enemy1
    """

    if enemy1.rect.x == enemy2.rect.x:
        if enemy1.rect.y > enemy2.rect.y:
            return -1
        else:
            return 1
    elif enemy1.rect.x < enemy2.rect.x:
        return -1
    else:
        return 1
