# WXQ
# 时间： $(DATE) $(TIME)
from item_2 import cal_size, find_homo_items, item
import math
from homo_position import Position


class package:
    def __init__(self, size_x, size_y):
        self.i = 0
        self.size_x = math.ceil(size_x * 2.84)
        self.size_y = math.ceil(size_y * 2.84)
        self.index = 0
        self.in_package = True
        # a=[self.size_y]*self.size_x
        # self.square = a
        self.level = 0  # 表示当前层的高度
        self.higt = 0  # 层的高度
        self.w = 0  # 已经占的高度
        self.start = 0  # 距离起始点的距离
        self.wight = 0  # 当前x轴上占的尺寸
        self.area = 0
        self.gap_wight = 0
        self.gap_high = 0
        self.homo_color_pre = -1
        self.pre_color = -1
        self.max_high = 0
        self.w_3 = 0  # 用于四阶段排列
        self.h = 0  # 表示四阶段中排列的高度

    def rot_package(self):
        self.size_y, self.size_x = self.size_x, self.size_y
        a = []
        for i in range(self.size_x):
            a.append(self.size_y)
        self.square = a

    def new_package(self, size_x, size_y):
        b = package(size_x, size_y)
        b.index = self.index + 1
        return b

    def compare_all_situation(self, size_x, size_y, size_first_fill, size_other, num_of_homo_item):  # 选择占用率最大的同质块排布方式
        if size_y > size_x:  # 如果y方向大于x方向
            short_size = size_x
            long_size = size_y
        else:
            short_size = size_y
            long_size = size_x
        if (size_first_fill < short_size or size_other < short_size) or (
                size_first_fill < long_size and size_other < long_size):
            return 0, 0, 0, 0

        best_short_num = 0
        num = int(size_first_fill / short_size)
        num_short = int(size_other / long_size)  # 在需要优先排满的方向上，不旋转所能排的最大数量
        num_long = int(size_other / short_size)  # 在需要优先排满的方向上，需要旋转所能排的最大数量
        best_rate = 0
        best_size_x = size_other
        best_size_y = size_first_fill
        used_num = 0  # 在第二方向能放下的数量
        best_used_num = 0
        for i in range(num + 1):
            if i * num_short > num_of_homo_item:
                break
            if i == 0:  # 完全按照长的情况排列
                if size_first_fill < long_size:  # 如果长向排布放不下
                    continue
                if num_long >= num_of_homo_item:  # 如果长的不够一排
                    used_y = long_size
                    used_x = num_of_homo_item * short_size
                    rate = (num_of_homo_item * short_size * long_size) / (size_first_fill * size_other)
                    used_num = 1
                    if rate > best_rate:  # 如果占用率能上升，选择这种排布方式
                        best_size_y = used_y
                        best_size_x = used_x
                        best_rate = rate
                        best_short_num = 0
                        best_used_num = used_num
                    elif rate == best_rate:
                        if used_y < best_size_y:  # 如果占用率虽然不能上升,但是能减少高度，排的跟密一些任然可以考虑
                            best_size_y = used_y
                            best_size_x = used_x
                            best_rate = rate
                            best_short_num = 0
                            best_used_num = used_num
                else:
                    a = int((num_of_homo_item - i * num_short) / num_long)  # 短边排完的情况下，按数量能排的长边数量
                    b = int((size_first_fill - i * short_size) / long_size)  # 按长度能拼进的长边的数量
                    long_can_put = min(a, b)  # 实际能拼进的个数
                    used_y = long_can_put * long_size
                    used_x = num_long * short_size
                    rate = (long_can_put * num_long * short_size * long_size) / (size_first_fill * size_other)
                    used_num = long_can_put
                    if rate > best_rate:  # 如果占用率能上升，选择这种排布方式
                        best_size_y = used_y
                        best_size_x = used_x
                        best_rate = rate
                        best_short_num = 0
                        best_used_num = used_num
                    elif rate == best_rate:
                        if used_y < best_size_y:  # 如果占用率虽然不能上升,但是能减少高度，排的跟密一些任然可以考虑
                            best_size_y = used_y
                            best_size_x = used_x
                            best_rate = rate
                            best_short_num = 0
                            best_used_num = used_num
                continue

            if num_short >= num_of_homo_item:  # 如果短的一排都排不满
                if size_first_fill < long_size:  # 如果拼不进长的
                    used_y = short_size
                    used_x = long_size * num_of_homo_item
                    best_short_num = 1
                    used_num = 1
                else:
                    used_y = long_size
                    used_x = short_size * num_of_homo_item
                    best_short_num = 0
                    used_num = 1
                return used_x, used_y, best_short_num, used_num
            elif (i * num_short) > num_of_homo_item:  # 如果连默认方向的都不能排满
                used_y = int(num_of_homo_item / num_short) * short_size  # 第二方向上能排的尺寸
                used_x = num_short * long_size
                rate = used_x * used_y / (int(num_of_homo_item / num_short) * short_size) * size_other
                used_num = int(num_of_homo_item / num_short)
                if rate > best_rate:  # 如果占用率能上升，选择这种排布方式
                    best_size_y = used_y
                    best_size_x = used_x
                    best_short_num = i
                    best_used_num = used_num
                elif rate == best_rate:
                    if used_y < best_size_y:  # 如果占用率虽然不能上升,但是能减少高度，排的跟密一些任然可以考虑
                        best_size_y = used_y
                        best_size_x = used_x
                        best_short_num = i
                        best_used_num = used_num
                return best_size_x, best_size_y, best_short_num, best_used_num
            else:  # 如果选择的短边数量能排满
                a = int((num_of_homo_item - i * num_short) / num_long)  # 短边排完的情况下，按数量能排的长边数量
                b = int((size_first_fill - i * short_size) / long_size)  # 按长度能拼进的长边的数量
                long_can_put = min(a, b)  # 实际能拼进的个数
                used_num = long_can_put + i
                used_y = i * short_size + long_can_put * long_size
                rate = ((i * num_short + long_can_put * num_long) * long_size * short_size) / (
                        size_first_fill * size_other)
                if long_can_put > 0:
                    used_x = max(num_short * long_size, num_long * short_size)
                else:
                    used_x = num_short * long_size

            if rate > best_rate:  # 如果占用率能上升，选择这种排布方式
                best_size_y = used_y
                best_size_x = used_x
                best_rate = rate
                best_short_num = i
                best_used_num = used_num
            elif rate == best_rate:
                if used_y < best_size_y:  # 如果占用率虽然不能上升,但是能减少高度，排的跟密一些任然可以考虑
                    best_size_y = used_y
                    best_size_x = used_x
                    best_rate = rate
                    best_short_num = i
                    best_used_num = used_num
        return best_size_x, best_size_y, best_short_num, best_used_num

    def find_homo_arrange(self, homo_items, gap_height, gap_width):
        homo_size_x = homo_items[0].size_x
        homo_size_y = homo_items[0].size_y
        size_x1, size_y1, num1, put_num1 = self.compare_all_situation(homo_size_x, homo_size_y, gap_height, gap_width,
                                                                      len(homo_items))
        size_y2, size_x2, num2, put_num2 = self.compare_all_situation(homo_size_x, homo_size_y, gap_width, gap_height,
                                                                      len(homo_items))
        if put_num1 == 0 and put_num2 == 0:
            return 0, 0, 0, 0, 0
        if put_num1 == 0:
            size_x1, size_y1 = 0, 0
        elif put_num2 == 0:
            size_y2, size_x2 = 0, 0
        if (size_x1 == gap_width and size_y1 <= gap_height) or (size_x1 <= gap_width and size_y1 == gap_height):
            size_x = size_x1
            size_y = size_y1
            num = num1
            put_num = put_num1
            direction = 0  # 0表示优先排x轴方向
        elif (size_x2 == gap_width and size_y2 <= gap_height) or (size_x2 <= gap_width and size_y2 == gap_height):
            size_x = size_x2
            size_y = size_y2
            num = num2
            put_num = put_num2
            direction = 1  # 1表示优先排y轴方向
        elif (gap_height - size_y1) > homo_size_x:  # 如果次优先拼接方向距离Gap距离越小，则选择这个拼接方向
            size_x = size_x2
            size_y = size_y2
            num = num2
            direction = 1
            put_num = put_num2
        else:
            size_x = size_x1
            size_y = size_y1
            num = num1
            put_num = put_num1
            direction = 0
        return size_x, size_y, num, direction, put_num

    def find_index_of_best_fit(self, items, gap_width, gap_height):
        best_index1 = -1
        best_index2 = -1
        best_num1 = 0
        best_num2 = 0
        index = 0
        best_direction1 = 0
        best_direction2 = 0
        best_fit_width1 = 0
        best_fit_width2 = 0
        best_put_num1 = 0
        best_put_num2 = 0
        number_of_squares = len(items)
        best_homo1 = False
        best_homo2 = False
        b = []

        for i in range(number_of_squares):  # 将所有位于这个大盒子的小盒子遍历完
            if i in b:  # 如果已经遍历过
                continue
            homo_items, _ = find_homo_items(items[i], i, items, b)
            color_cluster = items[i].color_cluster
            if len(homo_items) == 1:
                width = items[i].size_x
                height = items[i].size_y
                color_cluster = items[i].color_cluster
                num = 1
                homo = False
                put_num = 1
                direction = 0
            else:
                width, height, num, direction, put_num = self.find_homo_arrange(homo_items, gap_height, gap_width)
                # width, height, y, x, rotate = choice_rotate(homo_items, gap_height, gap_width)
                color_cluster = self.porp_color(homo_items)
                homo = True
                if width == 0 or height == 0 or put_num == 0:
                    homo = False
                    continue
            if ((width == gap_width and height <= gap_height) or (height == gap_width and width <= gap_height)) and (
                    self.pre_color == color_cluster):  # 只要把一面空隙填满，这个小盒子就是最优的盒子
                return i, num, direction, homo, put_num
            if self.pre_color == color_cluster:
                if (
                        width < gap_width and width > best_fit_width1 and height <= gap_height):  # 如果能找到比放在空隙里面最大的width还大的，那这个就是最优的小箱子
                    best_index1 = i
                    best_num1 = num
                    best_direction1 = direction
                    best_homo1 = homo
                    best_put_num1 = put_num
                    best_fit_width1 = width

                elif (
                        height < gap_width and height > best_fit_width1 and width <= gap_height):  # 同上，都是将width争取填满在考虑height
                    best_index1 = i
                    best_num1 = num
                    best_direction1 = direction
                    best_homo1 = homo
                    best_put_num1 = put_num
                    best_fit_width1 = height
            else:
                if (
                        width < gap_width and width > best_fit_width2 and height <= gap_height):  # 如果能找到比放在空隙里面最大的width还大的，那这个就是最优的小箱子
                    best_index2 = i
                    best_num2 = num
                    best_direction2 = direction
                    best_homo2 = homo
                    best_put_num2 = put_num
                    best_fit_width2 = width

                elif (
                        height < gap_width and height > best_fit_width2 and width <= gap_height):  # 同上，都是将width争取填满在考虑height
                    best_index2 = i
                    best_num2 = num
                    best_direction2 = direction
                    best_homo2 = homo
                    best_put_num2 = put_num
                    best_fit_width2 = height

        if best_index1 == -1:
            best_index = best_index2
            best_num = best_num2
            best_direction = best_direction2
            best_homo = best_homo2
            best_put_num = best_put_num2
        else:
            best_index = best_index1
            best_num = best_num1
            best_direction = best_direction1
            best_homo = best_homo1
            best_put_num = best_put_num1

        return best_index, best_num, best_direction, best_homo, best_put_num  # 返回能填这个width的最优小盒子的索引

    def put_in_y(self, items):
        self.w = 0
        self.higt = 0
        self.start = 0
        index, num, direction, homo, put_num = self.find_index_of_best_fit(items, self.size_x - self.level, self.size_y)
        if index == -1:
            self.in_package = False
            self.wight = 0
            return
        homo_items, homo_index = find_homo_items(items[index], index, items)
        if not homo:
            if (items[index].size_x <= self.size_x - self.level) & (items[index].size_y <= self.size_y):
                self.wight = items[index].size_x
                items[index].index = self.index
                items[index].position_y = 0
                items[index].position_x = self.level
                # self.square_change(0,items[index])
                self.wight = items[index].size_x
                self.start = items[index].size_y
                self.pre_color = items[index].color_cluster
                items.pop(index)

            else:
                items[index].rot_item()
                if (items[index].size_x <= self.size_x - self.level) & (items[index].size_y <= self.size_y):
                    self.wight = items[index].size_x
                    items[index].index = self.index
                    items[index].position_y = 0
                    items[index].position_x = self.level
                    # self.square_change(0,items[index])
                    self.wight = items[index].size_x
                    self.start = items[index].size_y
                    self.pre_color = items[index].color_cluster
                    items.pop(index)
        else:
            position_x, position_y, used_items = self.put_homo_block(items, homo_index, num, direction, put_num,
                                                                     self.size_x - self.level, self.size_y,
                                                                     self.level, self.start)
            self.start = position_y
            self.wight = position_x - self.level
            for i in reversed(used_items):
                items[i].index = self.index
                items.pop(i)

    def put_in_x(self, items):
        self.w = 0
        # index = self.find_index_of_best_fit(items, self.wight, self.size_y-self.start)
        index, num, direction, homo, put_num = self.find_index_of_best_fit(items, self.wight, self.size_y - self.start)
        if index == -1:
            self.level = self.level + self.wight
            if self.max_high < self.start:
                self.max_high = self.start
            self.put_in_y(items)
        else:
            homo_items, homo_index = find_homo_items(items[index], index, items)
            if not homo:
                if (items[index].size_y <= (self.size_y - self.start)) & (items[index].size_x <= self.wight) and (
                        items[index].size_x <= (self.size_y - self.start)) & (items[index].size_y <= self.wight):
                    if items[index].size_y > items[index].size_x:
                        items[index].rot_item()
                    items[index].index = self.index
                    items[index].position_y = self.start
                    items[index].position_x = self.level
                    # self.square_change(self.start,items[index])
                    self.higt = items[index].size_y
                    self.w = items[index].size_x
                    self.pre_color = items[index].color_cluster
                    items.pop(index)
                elif (items[index].size_y <= (self.size_y - self.start)) & (items[index].size_x <= self.wight):
                    items[index].index = self.index
                    items[index].position_y = self.start
                    items[index].position_x = self.level
                    # self.square_change(self.start,items[index])
                    self.higt = items[index].size_y
                    self.w = items[index].size_x
                    self.pre_color = items[index].color_cluster
                    items.pop(index)
                else:
                    items[index].rot_item()
                    if (items[index].size_y <= (self.size_y - self.start)) & (items[index].size_x <= self.wight):
                        items[index].index = self.index
                        items[index].position_y = self.start
                        items[index].position_x = self.level
                        # self.square_change(self.start,items[index])
                        self.higt = items[index].size_y
                        self.w = items[index].size_x
                        self.pre_color = items[index].color_cluster
                        items.pop(index)
            else:
                position_x, position_y, used_items = self.put_homo_block(items, homo_index, num, direction, put_num,
                                                                         self.wight, self.size_y - self.start,
                                                                         self.level, self.start)
                self.higt = position_y - self.start
                self.w = position_x - self.level
                for i in reversed(used_items):
                    items[i].index = self.index
                    items.pop(i)

    def put_in_3(self, items):
        # index = self.find_index_of_best_fit(items,self.wight-self.w,self.higt)
        index, num, direction, homo, put_num = self.find_index_of_best_fit(items, self.wight - self.w, self.higt)
        if index == -1:
            self.start = self.start + self.higt
            self.put_in_x(items)
        else:
            homo_items, homo_index = find_homo_items(items[index], index, items)
            if not homo:
                if ((self.wight - self.w) >= items[index].size_x) & (items[index].size_y <= self.higt) and (
                        (self.wight - self.w) >= items[index].size_y) & (items[index].size_x <= self.higt):
                    if items[index].size_x > items[index].size_y:
                        items[index].rot_item()
                    items[index].index = self.index
                    items[index].position_y = self.start
                    items[index].position_x = self.w + self.level
                    self.w_3 = items[index].size_x

                    # self.square_change(self.start, items[index])
                    self.h = items[index].size_y
                    self.pre_color = items[index].color_cluster
                    items.pop(index)

                elif ((self.wight - self.w) >= items[index].size_x) & (items[index].size_y <= self.higt):
                    items[index].index = self.index
                    items[index].position_y = self.start
                    items[index].position_x = self.w + self.level
                    self.w_3 = items[index].size_x
                    # self.square_change(self.start, items[index])
                    self.h = items[index].size_y
                    self.pre_color = items[index].color_cluster
                    items.pop(index)
                else:
                    items[index].rot_item()
                    if ((self.wight - self.w) >= items[index].size_x) & (items[index].size_y <= self.higt):
                        items[index].index = self.index
                        items[index].position_y = self.start
                        items[index].position_x = self.w + self.level
                        self.w_3 = items[index].size_x
                        self.h = items[index].size_y
                        # self.square_change(self.start, items[index])

                        self.pre_color = items[index].color_cluster
                        items.pop(index)
            else:
                position_x, position_y, used_items = self.put_homo_block(items, homo_index, num, direction, put_num,
                                                                         self.wight - self.w, self.higt,
                                                                         self.level + self.w, self.start)
                self.w_3 = position_x - self.w - self.level
                self.h = position_y - self.start
                for i in reversed(used_items):
                    items[i].index = self.index
                    items.pop(i)

    def put_in_4(self, items):
        # index = self.find_index_of_best_fit(items,self.wight-self.w,self.higt)
        index, num, direction, homo, put_num = self.find_index_of_best_fit(items, self.w_3, self.higt - self.h)
        if index == -1:
            self.w = self.w + self.w_3
            self.w_3 = 0
            self.h = 0
            self.put_in_3(items)
        else:
            homo_items, homo_index = find_homo_items(items[index], index, items)
            if not homo:
                if ((self.w_3) >= items[index].size_x) & (items[index].size_y <= (self.higt - self.h)) and (
                        (self.w_3) >= items[index].size_y) & (items[index].size_x <= (self.higt - self.h)):
                    if items[index].size_x > items[index].size_y:
                        items[index].rot_item()
                    items[index].index = self.index
                    items[index].position_y = self.start + self.h
                    items[index].position_x = self.w + self.level
                    # self.square_change(self.start, items[index])
                    self.h = self.h + items[index].size_y
                    self.pre_color = items[index].color_cluster
                    items.pop(index)

                elif ((self.w_3) >= items[index].size_x) & (items[index].size_y <= (self.higt - self.h)):
                    items[index].index = self.index
                    items[index].position_y = self.start + self.h
                    items[index].position_x = self.w + self.level
                    # self.square_change(self.start, items[index])
                    self.h = self.h + items[index].size_y
                    self.pre_color = items[index].color_cluster
                    items.pop(index)
                else:
                    items[index].rot_item()
                    if ((self.w_3) >= items[index].size_x) & (items[index].size_y <= (self.higt - self.h)):
                        items[index].index = self.index
                        items[index].position_y = self.start + self.h
                        items[index].position_x = self.w + self.level
                        # self.square_change(self.start, items[index])
                        self.h = self.h + items[index].size_y
                        self.pre_color = items[index].color_cluster
                        items.pop(index)
            else:
                position_x, position_y, used_items = self.put_homo_block(items, homo_index, num, direction, put_num,
                                                                         self.w_3, self.higt - self.h,
                                                                         self.level + self.w, self.start + self.h)
                self.h = position_y - self.start
                for i in reversed(used_items):
                    items[i].index = self.index
                    items.pop(i)

    def find_same_color(self, items, homo_index, used_index, new_line):
        index = -1
        if self.homo_color_pre == -1:
            for i in homo_index:
                if i in used_index:
                    continue
                if items[i].color_cluster == self.pre_color:
                    return i

        for i in homo_index:
            if i in used_index:
                continue
            if items[i].color_cluster == self.homo_color_pre:
                return i
            else:
                index = i
        return index

    def put_homo_block(self, items, b, num, direction, num_1, gap_width, gap_height, position_x, position_y):
        used_items = []
        last_color_label = -1
        if direction == 0:
            max_px = position_x
            max_py = position_y
            if items[b[0]].size_x > items[b[0]].size_y:
                long_size = items[b[0]].size_x
                short_size = items[b[0]].size_y
            else:
                long_size = items[b[0]].size_y
                short_size = items[b[0]].size_x
                rotate_homo(items, b)


            max_long = int(gap_width / short_size)
            max_short = int(gap_width / long_size)
            indexs = resort(items, b, num, num_1, direction, max_long, max_short)
            items_position = count(long_size, short_size, gap_width, gap_height, num, num_1, position_x, position_y,direction)  # 获取同质块中所有可排入位置的坐标
            positions = create_position(items_position, short_size, long_size, max_long, max_short, num, num_1,
                                        direction)
            positions = resort_position_id(positions)
            new_row_index = find_new_row_num(positions)
            used_position = []
            last_position = -1#用于记录上一个item存放的地址
            while len(positions) > len(used_position) and len(indexs) != 0:
                if items[indexs[0]].color_cluster != last_color_label and len(new_row_index ) != 0 :#如果出现新的颜色，并且还有新的行,那么提行
                    if positions[new_row_index[0]].rotate:
                        items[indexs[0]].rot_item()
                        items[indexs[0]].index = self.index
                        items[indexs[0]].position_x = positions[new_row_index[0]].position_x
                        items[indexs[0]].position_y = positions[new_row_index[0]].position_y
                        max_px = max(positions[new_row_index[0]].position_x +items[indexs[0]].size_x, max_px)
                        max_py = max(positions[new_row_index[0]].position_y + items[indexs[0]].size_y, max_py)
                        self.homo_color_pre = items[b[0]].color_cluster
                        used_items.append(indexs[0])
                        used_position.append(new_row_index[0])
                        last_position = new_row_index[0]
                        last_color_label = items[indexs[0]].color_cluster
                        new_row_index.pop(0)
                        indexs.pop(0)
                    else:
                        items[indexs[0]].index = self.index
                        items[indexs[0]].position_x = positions[new_row_index[0]].position_x
                        items[indexs[0]].position_y = positions[new_row_index[0]].position_y
                        max_px = max(positions[new_row_index[0]].position_x + items[indexs[0]].size_x, max_px)
                        max_py = max(positions[new_row_index[0]].position_y + items[indexs[0]].size_y, max_py)
                        self.homo_color_pre = items[indexs[0]].color_cluster
                        used_items.append(indexs[0])
                        used_position.append(new_row_index[0])
                        last_position = new_row_index[0]
                        last_color_label = items[indexs[0]].color_cluster
                        new_row_index.pop(0)
                        indexs.pop(0)
                elif items[indexs[0]].color_cluster != last_color_label : #如果和前一个颜色不同，并且没有新的行了，那么优先对前面剩下的空位进行补齐
                    for i in range(len(positions)):
                        if i not in used_position:
                            if positions[i].rotate:
                                items[indexs[0]].rot_item()
                                items[indexs[0]].index = self.index
                                items[indexs[0]].position_x = positions[i].position_x
                                items[indexs[0]].position_y = positions[i].position_y
                                max_px = max(positions[i].position_x + items[indexs[0]].size_x, max_px)
                                max_py = max(positions[i].position_y + items[indexs[0]].size_y, max_py)
                                self.homo_color_pre = items[indexs[0]].color_cluster
                                used_items.append(indexs[0])
                                used_position.append(i)
                                last_position = i
                                last_color_label = items[indexs[0]].color_cluster
                                indexs.pop(0)
                            else:
                                items[indexs[0]].index = self.index
                                items[indexs[0]].position_x = positions[i].position_x
                                items[indexs[0]].position_y = positions[i].position_y
                                max_px = max(positions[i].position_x + items[indexs[0]].size_x, max_px)
                                max_py = max(positions[i].position_y + items[indexs[0]].size_y, max_py)
                                self.homo_color_pre = items[indexs[0]].color_cluster
                                used_items.append(indexs[0])
                                used_position.append(i)
                                last_position = i
                                last_color_label = items[indexs[0]].color_cluster
                                indexs.pop(0)
                            break
                else: # 如果与之前的颜色一致，那么排在上一个position的后面
                    last_position += 1
                    if last_position >= len(positions):#如果相同颜色的排不下了，考虑以前中间空缺的
                        for i in range(len(positions)):
                            if i not in used_position:
                                if positions[i].rotate:
                                    items[indexs[0]].rot_item()
                                    items[indexs[0]].index = self.index
                                    items[indexs[0]].position_x = positions[i].position_x
                                    items[indexs[0]].position_y = positions[i].position_y
                                    max_px = max(positions[i].position_x + items[indexs[0]].size_x, max_px)
                                    max_py = max(positions[i].position_y + items[indexs[0]].size_y, max_py)
                                    self.homo_color_pre = items[indexs[0]].color_cluster
                                    used_items.append(indexs[0])
                                    used_position.append(i)
                                    last_position = i
                                    last_color_label = items[indexs[0]].color_cluster
                                    indexs.pop(0)
                                else:
                                    items[indexs[0]].index = self.index
                                    items[indexs[0]].position_x = positions[i].position_x
                                    items[indexs[0]].position_y = positions[i].position_y
                                    max_px = max(positions[i].position_x + items[indexs[0]].size_x, max_px)
                                    max_py = max(positions[i].position_y + items[indexs[0]].size_y, max_py)
                                    self.homo_color_pre = items[indexs[0]].color_cluster
                                    used_items.append(indexs[0])
                                    used_position.append(i)
                                    last_position = i
                                    last_color_label = items[indexs[0]].color_cluster
                                    indexs.pop(0)
                                break
                        continue
                    if last_position in new_row_index:#如果放置在了新的一列
                        new_row_index.pop(0)
                    if positions[last_position].rotate:
                        items[indexs[0]].rot_item()
                        items[indexs[0]].index = self.index
                        items[indexs[0]].position_x = positions[last_position].position_x
                        items[indexs[0]].position_y = positions[last_position].position_y
                        max_px = max(positions[last_position].position_x + items[indexs[0]].size_x, max_px)
                        max_py = max(positions[last_position].position_y + items[indexs[0]].size_y, max_py)
                        self.homo_color_pre = items[indexs[0]].color_cluster
                        used_items.append(indexs[0])
                        used_position.append(last_position)
                        last_color_label = items[indexs[0]].color_cluster
                        indexs.pop(0)
                    else:
                        items[indexs[0]].index = self.index
                        items[indexs[0]].position_x = positions[last_position].position_x
                        items[indexs[0]].position_y = positions[last_position].position_y
                        max_px = max(positions[last_position].position_x + items[indexs[0]].size_x, max_px)
                        max_py = max(positions[last_position].position_y + items[indexs[0]].size_y, max_py)
                        self.homo_color_pre = items[indexs[0]].color_cluster
                        used_items.append(indexs[0])
                        used_position.append(last_position)
                        last_color_label = items[indexs[0]].color_cluster
                        indexs.pop(0)
            used_items = sorted(used_items)
            self.homo_color_pre = -1
            return max_px, max_py, used_items
        else:
            max_py = position_y
            max_px = position_x
            if items[b[0]].size_x > items[b[0]].size_y:
                long_size = items[b[0]].size_x
                short_size = items[b[0]].size_y
                rotate_homo(items, b)
            else:
                long_size = items[b[0]].size_y
                short_size = items[b[0]].size_x
            max_long = int(gap_height / short_size)
            max_short = int(gap_height / long_size)

            indexs = resort(items, b, num, num_1, direction, max_long, max_short)
            items_position = count(long_size, short_size, gap_width, gap_height, num, num_1, position_x, position_y,
                                   direction)  # 获取同质块中所有可排入位置的坐标
            positions = create_position(items_position, short_size, long_size, max_long, max_short, num, num_1,
                                        direction)
            positions = resort_position_id(positions)
            new_row_index = find_new_row_num(positions)
            used_position = []
            last_position = -2  # 用于记录上一个item存放的地址
            while len(positions) > len(used_position) and len(indexs) != 0:
                if items[indexs[0]].color_cluster != last_color_label and len(new_row_index) != 0:  # 如果出现新的颜色，并且还有新的行,那么提行
                    if positions[new_row_index[0]].rotate:
                        items[indexs[0]].rot_item()
                        items[indexs[0]].index = self.index
                        items[indexs[0]].position_x = positions[new_row_index[0]].position_x
                        items[indexs[0]].position_y = positions[new_row_index[0]].position_y
                        max_px = max(positions[new_row_index[0]].position_x + items[indexs[0]].size_x, max_px)
                        max_py = max(positions[new_row_index[0]].position_y + items[indexs[0]].size_y, max_py)
                        self.homo_color_pre = items[indexs[0]].color_cluster
                        used_items.append(indexs[0])
                        used_position.append(new_row_index[0])
                        last_position = new_row_index[0]
                        last_color_label = items[indexs[0]].color_cluster
                        new_row_index.pop(0)
                        indexs.pop(0)
                    else:
                        items[indexs[0]].index = self.index
                        items[indexs[0]].position_x = positions[new_row_index[0]].position_x
                        items[indexs[0]].position_y = positions[new_row_index[0]].position_y
                        max_px = max(positions[new_row_index[0]].position_x + items[indexs[0]].size_x, max_px)
                        max_py = max(positions[new_row_index[0]].position_y + items[indexs[0]].size_y, max_py)
                        self.homo_color_pre = items[indexs[0]].color_cluster
                        used_items.append(indexs[0])
                        used_position.append(new_row_index[0])
                        last_position = new_row_index[0]
                        last_color_label = items[indexs[0]].color_cluster
                        new_row_index.pop(0)
                        indexs.pop(0)
                elif items[indexs[0]].color_cluster != last_color_label:  # 如果和前一个颜色不同，并且没有新的行了，那么优先对前面剩下的空位进行补齐
                    for i in range(len(positions)):
                        if i not in used_position:
                            if positions[i].rotate:
                                items[indexs[0]].rot_item()
                                items[indexs[0]].index = self.index
                                items[indexs[0]].position_x = positions[i].position_x
                                items[indexs[0]].position_y = positions[i].position_y
                                max_px = max(positions[i].position_x + items[indexs[0]].size_x, max_px)
                                max_py = max(positions[i].position_y + items[indexs[0]].size_y, max_py)
                                self.homo_color_pre = items[indexs[0]].color_cluster
                                used_items.append(indexs[0])
                                used_position.append(i)
                                last_position = i
                                last_color_label = items[indexs[0]].color_cluster
                                indexs.pop(0)
                            else:
                                items[indexs[0]].index = self.index
                                items[indexs[0]].position_x = positions[i].position_x
                                items[indexs[0]].position_y = positions[i].position_y
                                max_px = max(positions[i].position_x + items[indexs[0]].size_x, max_px)
                                max_py = max(positions[i].position_y + items[indexs[0]].size_y, max_py)
                                self.homo_color_pre = items[indexs[0]].color_cluster
                                used_items.append(indexs[0])
                                used_position.append(i)
                                last_position = i
                                last_color_label = items[indexs[0]].color_cluster
                                indexs.pop(0)
                            break
                else:  # 如果与之前的颜色一致，那么排在上一个position的后面
                    last_position += 1
                    if last_position in used_position:
                        continue
                    if last_position >= len(positions):#如果相同颜色的排不下了，考虑以前中间空缺的
                        for i in range(len(positions)):
                            if i not in used_position:
                                if positions[i].rotate:
                                    items[indexs[0]].rot_item()
                                    items[indexs[0]].index = self.index
                                    items[indexs[0]].position_x = positions[i].position_x
                                    items[indexs[0]].position_y = positions[i].position_y
                                    max_px = max(positions[i].position_x + items[indexs[0]].size_x, max_px)
                                    max_py = max(positions[i].position_y + items[indexs[0]].size_y, max_py)
                                    self.homo_color_pre = items[indexs[0]].color_cluster
                                    used_items.append(indexs[0])
                                    used_position.append(i)
                                    last_position = i
                                    last_color_label = items[indexs[0]].color_cluster
                                    indexs.pop(0)
                                else:
                                    items[indexs[0]].index = self.index
                                    items[indexs[0]].position_x = positions[i].position_x
                                    items[indexs[0]].position_y = positions[i].position_y
                                    max_px = max(positions[i].position_x + items[indexs[0]].size_x, max_px)
                                    max_py = max(positions[i].position_y + items[indexs[0]].size_y, max_py)
                                    self.homo_color_pre = items[indexs[0]].color_cluster
                                    used_items.append(indexs[0])
                                    used_position.append(i)
                                    last_position = i
                                    last_color_label = items[indexs[0]].color_cluster
                                    indexs.pop(0)
                                break
                        continue
                    if last_position in new_row_index:  # 如果放置在了新的一列
                        new_row_index.pop(0)
                    if positions[last_position].rotate:
                        items[indexs[0]].rot_item()
                        items[indexs[0]].index = self.index
                        items[indexs[0]].position_x = positions[last_position].position_x
                        items[indexs[0]].position_y = positions[last_position].position_y
                        max_px = max(positions[last_position].position_x + items[indexs[0]].size_x, max_px)
                        max_py = max(positions[last_position].position_y + items[indexs[0]].size_y, max_py)
                        self.homo_color_pre = items[indexs[0]].color_cluster
                        used_items.append(indexs[0])
                        used_position.append(last_position)
                        last_color_label = items[indexs[0]].color_cluster
                        indexs.pop(0)
                    else:
                        items[indexs[0]].index = self.index
                        items[indexs[0]].position_x = positions[last_position].position_x
                        items[indexs[0]].position_y = positions[last_position].position_y
                        max_px = max(positions[last_position].position_x + items[indexs[0]].size_x, max_px)
                        max_py = max(positions[last_position].position_y + items[indexs[0]].size_y, max_py)
                        self.homo_color_pre = items[indexs[0]].color_cluster
                        used_items.append(indexs[0])
                        used_position.append(last_position)
                        last_color_label = items[indexs[0]].color_cluster
                        indexs.pop(0)
            used_items = sorted(used_items)
            self.homo_color_pre = -1
            return max_px, max_py, used_items

    # def fill(self, size_x, size_y, b, items):
    #     best_index = -1
    #     index = 0
    #     best_fit_width = 0
    #     number_of_squares = len(items)
    #
    #     while (index < number_of_squares):  # 将所有位于这个大盒子的小盒子遍历完
    #         if index in b:
    #             index += 1
    #             continue
    #         width = items[index].size_x
    #         height = items[index].size_y
    #
    #         if (width == size_x and height <= size_y) or (
    #                 height == size_x and width <= size_y):  # 只要把一面空隙填满，这个小盒子就是最优的盒子
    #             return index
    #
    #         if (width < size_x and width > best_fit_width and height <= size_y):  # 如果能找到比放在空隙里面最大的width还大的，那这个就是最优的小箱子
    #             best_index = index
    #             best_fit_width = width
    #
    #         elif (height < size_x and height > best_fit_width and width <= size_y):  # 同上，都是将width争取填满在考虑height
    #             best_index = index
    #             best_fit_width = height
    #         index += 1
    #
    #     return best_index  # 返回能填这个width的最优小盒子的索引

    def porp_color(self, homo_items):
        for i in range(len(homo_items)):
            if homo_items[i].color_cluster == self.pre_color:
                return self.pre_color

        return homo_items[0].color_cluster


def choice_rotate(items, gap_high, gap_weight):
    num = len(items)
    rotate = False
    size_x1, size_y1 = cal_size(items[0].size_x, items[0].size_y, num, gap_high, gap_weight)
    size_x2, size_y2 = cal_size(items[0].size_y, items[0].size_x, num, gap_high, gap_weight)
    if (size_x1 + size_y1) >= (size_x2 + size_y2):
        size_x = size_x1
        size_y = size_y1
        num_y = size_y / items[0].size_y
        num_x = size_x / items[0].size_x
    else:
        size_x = size_x2
        size_y = size_y2
        num_y = size_y / items[0].size_x
        num_x = size_x / items[0].size_y
        rotate = True
    return size_x, size_y, num_y, num_x, rotate


def rotate_homo(items, indexs):
    for i in indexs:
        items[i].rot_item()


def sort_same_item(items, homo_indexs):
    used_index = []
    all_homo = []  # 用来存所有的homo_item
    # 根据相同订单的数量进行排序
    for i in range(len(homo_indexs)):  # 用来遍历所有的同质块，找到其中的相同订单
        if homo_indexs[i] in used_index:
            continue
        same_item = [homo_indexs[i]]
        used_index.append(homo_indexs[i])
        for j in range(i, len(homo_indexs)):
            if j == i:
                continue
            if items[homo_indexs[i]].location == items[homo_indexs[j]].location:
                same_item.append(homo_indexs[j])
                used_index.append(homo_indexs[j])
        same_item.sort(key=lambda x: items[x].page, reverse=True)  # 同一个订单中的Item根据按照页数进行排序
        all_homo.append(same_item)
    all_homo.sort(key=lambda x: len(x), reverse=True)  # 按照相同订单的类型的数量进行排序

    # 在根据颜色的分类对根据订单数量分类的进行排序
    used = []
    all_homo_2 = []
    same_color_item = []  # 用于存放所有相同颜色的item
    for i in range(len(all_homo)):
        if i in used:
            continue
        used.append(i)
        b = all_homo[i]  # 用于存放相同颜色的Item
        for j in range(i, len(all_homo)):
            if i == j or (j in used):
                continue
            if items[all_homo[i][0]].color_cluster == items[all_homo[j][0]].color_cluster:
                used.append(j)
                for n in range(len(all_homo[j])):
                    b.append(all_homo[j][n])
        same_color_item.append(b)
    same_color_item.sort(key=lambda x: len(x), reverse=True)  # 按照相同订单的类型的数量进行排序
    a = []
    for i in range(len(same_color_item)):
        for j in range(len(same_color_item[i])):
            a.append(same_color_item[i][j])
    return a


def resort(items, homo_indexs, num, num_1, direction, max_long, max_short):
    new_index = sort_same_item(items, homo_indexs)  # 根据颜色和数量进行排序
    label = []
    for i in range(len(new_index)):
        label.append(items[new_index[i]].color_cluster)

    if num_1 == 1:
        return new_index

    if direction == 0:  # 如果是按照横向排列
        a = max_short * num  # 正常放置的数量
        b = max_long * (num_1 - num)  # 旋转放置的数量
        a_index = [-1] * a
        b_index = [-1] * b
        index = 0

        for i in range(max_short):  # 对序列按照纵向重新排列
            for j in range(num):
                a_index[i + max_short * j] = new_index[index]
                index += 1

        for i in range(max_long):
            for j in range(num_1 - num):
                b_index[i + (max_long) * j] = new_index[index]
                index += 1
        put_index = []
        for i in range(len(a_index)):
            put_index.append(a_index[i])
        for i in range(len(b_index)):
            put_index.append(b_index[i])
    else:
        put_index = new_index
    return put_index


def count(x, y, gap_width, gap_height, num, num_1, position_x, position_y,direction):
    """
    :param x: 长度
    :param y: 宽度
    :param num_x: 横着的数量
    :param num_y: 竖着的数量
    :param num:  横着的高数量
    :param num_1:  总的高的数量
    :param position_x:  底角x
    :param position_y:  底角y
    :return:
    """
    """
       :param x: 长度
       :param y: 宽度
       :param num_x: 横着的数量
       :param num_y: 竖着的数量
       :param num:  横着的高数量
       :param num_1:  总的高的数量
       :param position_x:  底角x
       :param position_y:  底角y
       :return:
       """
    vertical_num = num_1 - num
    vertical_num_y = 0
    vertical_num_x = 0
    count_x = 0
    count_y = 0  # 要计算的xy
    horizontal = []  # 空列表
    horizontal_all = []  # 空列表
    horizontal_num_y = 0
    horizontal_num_x = 0
    # 计算横着的所有坐标
    if direction == 0:
        num_x = int(gap_width/x)
        num_y = int(gap_width/y)
        if num != 0:  # 有横着放的
            while horizontal_num_y < num:
                count_y = position_y + horizontal_num_y * y
                horizontal_num_y += 1
                horizontal_num_x = 0
                while horizontal_num_x < num_x:
                    count_x = position_x + horizontal_num_x * x
                    horizontal.append(count_y)
                    horizontal.append(count_x)
                    horizontal_all.append(horizontal[-1:-3:-1])
                    horizontal_num_x += 1
        # 计算竖着的所有坐标
        if num_1 - num != 0:  # 有竖着放的
            while vertical_num_y < vertical_num:
                count_y = position_y + num * y + vertical_num_y * x
                vertical_num_y += 1
                vertical_num_x = 0
                while vertical_num_x < num_y:
                    count_x = position_x + vertical_num_x * y
                    horizontal.append(count_y)
                    horizontal.append(count_x)
                    horizontal_all.append(horizontal[-1:-3:-1])
                    vertical_num_x += 1
    if direction == 1:
        num_x = int(gap_height / y)
        num_y = int(gap_height / x)
        if num != 0:  # 有横着放的
            while horizontal_num_x < num:
                count_x = position_x + horizontal_num_x * y
                horizontal_num_x += 1
                horizontal_num_y = 0
                while horizontal_num_y < num_y:
                    count_y = position_y + horizontal_num_y * x
                    horizontal.append(count_y)
                    horizontal.append(count_x)
                    horizontal_all.append(horizontal[-1:-3:-1])
                    horizontal_num_y += 1
        # 计算竖着的所有坐标
        if num_1 - num != 0:  # 有竖着放的
            while vertical_num_x < vertical_num:
                count_x = position_x +num * y + vertical_num_x * x
                vertical_num_x += 1
                vertical_num_y = 0
                while vertical_num_y < num_x:
                    count_y = position_y + vertical_num_y * y
                    horizontal.append(count_y)
                    horizontal.append(count_x)
                    horizontal_all.append(horizontal[-1:-3:-1])
                    vertical_num_y += 1
    return horizontal_all


def create_position(items_position, short_size, long_size, max_long, max_short, num, num_1, direction):  # 创建package对象
    """

    :param items_position:  item 能够排入的位置坐标
    :param short_size:  item的短边长度
    :param long_size: 长边长度
    :param max_long: 按长边放置能放入的最大数量
    :param max_short: 按短边放置能放入的最大数量
    :param num: 按短边放置的横排数量
    :param num_1: 总的横排数量
    :param direction: 优先排列的方向
    :return:
    """
    positions = []
    if direction == 0:
        items_size_h = [[long_size, short_size] ]* max_short * num
        items_size_v = [[short_size, long_size]] * max_long * (num_1 - num)
        items_size = items_size_h+items_size_v
        for i in range(len(items_size)):
            a = Position(i, items_position[i][0], items_position[i][1], long_size, short_size)
            if items_size[i][0] >= items_size[i][1]:
                positions.append(a)
            else:
                a.pos_rotate()
                positions.append(a)
    elif direction == 1:
        items_size_v = [[short_size, long_size]] * max_short * num
        items_size_h = [[long_size, short_size]] * max_long * (num_1 - num)
        items_size = items_size_v + items_size_h
        for i in range(len(items_size)):
            a = Position(i, items_position[i][0], items_position[i][1], long_size, short_size)
            if items_size[i][0] <= items_size[i][1]:
                positions.append(a)
            else:
                a.pos_rotate()
                positions.append(a)

    return positions


def resort_position_id(positions):
    new_positions = []

    while len(positions) != 0: #对所有的位置按照列数排序
        positions.sort(key=lambda x: (x.position_x, x.position_y)) #先对x轴坐标排序，在按照Y轴排序
        size_x = positions[0].size_x
        position_x = positions[0].position_x
        positions[0].new_row = True

        same_row_position = [positions[0]] #用于记录处于当前列中的item
        same_row_position_index = [0] #用于记录处于当前列中的id
        for i in range(1,len(positions)):
            if (positions[i].size_x/2 + positions[i].position_x) <= (position_x+size_x): #如果上面的item一半都位于当前的列中，则属于这个列中
                same_row_position.append(positions[i])
                same_row_position_index.append(i)
            else:
                break
        same_row_position.sort(key=lambda x: (x.position_y,x.position_x)) # 对同一列的先按照y轴排序在按照x轴排序
        same_row_position_index.sort(key= lambda x:x,reverse=True) #由大到小排序，方便pop
        for i in range(len(same_row_position_index)):
            positions.pop(same_row_position_index[i])
            new_positions.append(same_row_position[i])

    return new_positions

def find_new_row_num(positions):
    new_row_index = []
    for i in range(len(positions)):
        if positions[i].new_row :
            new_row_index.append(i)
    return new_row_index




