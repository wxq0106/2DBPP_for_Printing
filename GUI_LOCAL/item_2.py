# WXQ
# 时间： $(DATE) $(TIME)
import numpy as np
from pypdf import PdfReader, PdfWriter, Transformation, PaperSize
import math


class item:
    def __init__(self, location, size_x=0, size_y=0, page=0,rgb = [-1,-1,-1], color_cluster=-1, character=0, models=1):
        # self.size_x = size_x
        # self.size_y = size_y
        self.location = location  # 订单存储的位置
        # reader = PdfReader(self.location)
        # sourcepage = reader.pages[0]
        self.size_x = size_x  # 订单尺寸
        self.size_y = size_y
        self.square = self.size_y * self.size_x  # 订单面积
        self.max_len = max(self.size_y, self.size_x)
        self.total_len = self.size_x + self.size_y
        self.position_x = 0  # 订单页面在大版中位置
        self.position_y = 0
        self.sequence = -1  # 订单编号
        self.index = -1  # 订单所处的大版序号
        self.rotate = False
        self.color_cluster = color_cluster  # 订单对象的颜色分类
        self.rgb = rgb
        self.page = page  # 在订单对象中的页数
        self.character = character  # 订单对象的类型，DM单还是名片
        self.models = models  # 单个订单对象模数

    def copy_item(self):
        a = item(self.location, self.size_x, self.size_y, self.page, self.rgb, self.color_cluster)
        return a

    def get_square(self):
        self.square = self.size_x * self.size_y

    def get_size(self):
        reader = PdfReader(self.location)
        sourcepage = reader.pages[0]
        self.size_x = math.ceil(sourcepage.mediabox.upper_right[0])
        self.size_y = math.ceil(sourcepage.mediabox.upper_right[1])

    # def set_size(self):
    #     reader = PdfReader(self.location)
    #     sourcepage = reader.pages[0]
    #     self.size_x = sourcepage.mediabox.upper_right[0]
    #     self.size_y =sourcepage.mediabox.upper_right[1]

    def order_len(squares):
        squares.sort(key=lambda x: x.max_len, reverse=True)
        a = []
        for i in range(len(squares)):
            a.append(squares[i].sequence)
        return a

    def order_square(squares):
        squares.sort(key=lambda x: x.square, reverse=True)
        a = []
        for i in range(len(squares)):
            a.append(squares[i].sequence)
        return a

    def order_totallen(squares):
        squares.sort(key=lambda x: x.total_len, reverse=True)
        a = []
        for i in range(len(squares)):
            a.append(squares[i].sequence)
        return a

    def rot_item(self):
        self.size_y, self.size_x = self.size_x, self.size_y
        self.rotate = not self.rotate


def cal_size(x, y, num, gap_high, gap_weight):
    # x = items[0].size_x
    # y = items[0].size_y
    # num = len(items)
    a = math.modf(math.sqrt(num))[1]  # 计算如果按横向纵向数量一致排列，最大完整排列的数量
    if a < math.sqrt(num):
        a += 1
    num_x = int(gap_weight / x)  # 横向最多能放入同质块的个数
    num_y = int(gap_high / y)  # 纵向最多能放入同质块的个数
    if (num_x <= 0) or (num_y <= 0):
        return 0, 0
    b = min(num_x, num_y)  # 横向和纵向最少能放入的数量
    if a < b:  # 如果可以按照横向纵向数量相同放入
        size_y = y * math.ceil(num / a)
        size_x = x * a
    else:  # 如果不能按照数量相同放入
        if num_y < num_x:  # 如果能放入的纵向更少，那么优先将纵向放满
            size_y = num_y * y
            if math.ceil(num / num_y) <= num_x:  # 如果需要放入的横向数量小于最大能放入的个数
                size_x = math.ceil(num / num_y) * x
            else:
                size_x = num_x * x
        else:  # 优先将横向放满
            size_x = num_x * x
            if math.ceil(num / num_x) <= num_y:
                size_y = math.ceil(num / num_x) * y
            else:
                size_y = num_y * y
    if size_x > gap_weight or size_y > gap_high:
        print("chuwenti ")
    return size_x, size_y


def find_homo_items(ITEM, num, items, b=[]):  # 找到对应ITEM的同质块
    a = []
    c = []
    for i in range(num, len(items)):
        if ITEM.size_x == items[i].size_x and ITEM.size_y == items[i].size_y:
            a.append(items[i])
            b.append(i)
            c.append(i)
        elif ITEM.size_x == items[i].size_y and ITEM.size_y == items[i].size_x:
            items[i].rot_item()
            a.append(items[i])
            b.append(i)
            c.append(i)
    return a, c


def re_rotate(items):
    for i in range(len(items)):
        items[i].rotate = False
