# WXQ
# 时间： $(DATE) $(TIME)
class Position:
    def __init__(self, index, position_x, position_y, size_x, size_y):
        self.index = index
        self.position_x = position_x
        self.position_y = position_y
        self.size_x = size_x
        self.size_y = size_y
        self.new_row = False
        self.rotate = False

    def pos_rotate(self):
        self.rotate = not self.rotate
