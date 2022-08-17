from enemies import Enemy


class Beetle(Enemy):
    def __init__(self, pos):
        super().__init__("beetle", "", pos)
