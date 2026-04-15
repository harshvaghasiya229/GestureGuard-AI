class Smoother:
    def __init__(self, alpha=0.2):
        self.alpha = alpha
        self.prev_x = 0
        self.prev_y = 0

    def smooth(self, x, y):
        sx = int(self.prev_x + (x - self.prev_x) * self.alpha)
        sy = int(self.prev_y + (y - self.prev_y) * self.alpha)

        self.prev_x, self.prev_y = sx, sy
        return sx, sy