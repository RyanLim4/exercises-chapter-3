class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __contains__(self, point):
        from math import sqrt
        # find dist between point and center
        dist = sqrt((point[0] - self.center[0])**2 +
                    (point[1] - self.center[1])**2)
        if dist < self.radius:
            return True
        else:
            return False
