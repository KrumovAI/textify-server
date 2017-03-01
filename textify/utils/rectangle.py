class Rectangle:
    def __init__(self, x, y, width, height, contour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.contour = contour

    def contains(self, rect):
        if self.x <= rect.x and self.y <= rect.y:
            if self.x + self.width >= rect.x + rect.width:
                if self.y + self.height >= rect.y + rect.height:
                    return True

        return False

    def equals(self, other):
        if self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height:
            return True

        return False

    def to_string(self):
        return "X: " + str(self.x) + "; Y: " + str(self.y) + "; Width: " + str(self.width) + \
               "; Height: " + str(self.height)
