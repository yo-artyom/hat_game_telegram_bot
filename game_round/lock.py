from utils.meta_singleton import MetaSingleton

class Lock(metaclass = MetaSingleton):
    def __init__(self):
        self.free = True
        self.blocked_by = None

    def obtain(self, player):
        self.free = False
        self.blocked_by = player

    def release(self):
        self.free = True
        self.player = None
