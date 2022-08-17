from enemies import Enemy


class Bloopa(Enemy):
    def __init__(self, pos):
        super().__init__("bloopa", "", pos)
