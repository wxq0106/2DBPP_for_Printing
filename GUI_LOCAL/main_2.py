# WXQ
# 时间： $(DATE) $(TIME)
from geneticsAlgoritham_2 import GeneticsAlgoritham
from In_Package_2 import in_package
from item_2 import item
import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from PyPDF3 import PdfFileWriter, PdfFileReader
from PyPDF3.pdf import PageObject
from classify_color import classify, read_sql
import json
from wire import wire
from PyQt5.QtCore import *  # 导入线程相关模块
import time
import subprocess
import datetime





def use_genetics(sign, items, generation_size, recombination, mutation, max_generations,
                 stop_criterium, package_order, cut_in_y, label):  # 使用遗传算法
    ga = GeneticsAlgoritham(sign, generation_size, recombination, mutation, max_generations, stop_criterium,
                            items, package_order, cut_in_y, label)
    best_chromosome = ga.find_best_solution()  # 找到最优解
    _, items, packages = in_package(items, best_chromosome.gene, cut_in_y, package_order, False)

    # bin.pack_squares_in_bins()

    return ga.log, best_chromosome.gene, items, packages


def find_line_position(items, line_size):
    wires = []
    for i in range(len(items)):
        position = get_position(items[i])#得到4个角坐标
        line_position = get_line_position(position, line_size[0], line_size[1])#得到绞线末尾坐标
        determine = [False] * 8
        for j in range(len(items)):
            if i == j:
                continue
            determine_interner(items[j], line_position, determine)#判断是否与其他边相交
        get_wire_object(position, determine, wires, line_size[0], line_size[1])
    return wires


def get_wire_object(position, determine, wires, line_x, line_y):
    if not determine[0]:
        wires.append(wire(position[0][0] - line_x, position[0][1], False))
    if not determine[1]:
        wires.append(wire(position[0][0], position[0][1] - line_x, True))
    if not determine[2]:
        wires.append(wire(position[1][0] - line_y, position[1][1] - line_x, True))
    if not determine[3]:
        wires.append(wire(position[1][0], position[1][1], False))
    if not determine[4]:
        wires.append(wire(position[2][0], position[2][1] - line_y, False))
    if not determine[5]:
        wires.append(wire(position[2][0] - line_y, position[2][1], True))
    if not determine[6]:
        wires.append(wire(position[3][0], position[3][1], True))
    if not determine[7]:
        wires.append(wire(position[3][0] - line_x, position[3][1] - line_y, False))


def get_position(item):
    position = [[item.position_x, item.position_y],  # 左下坐标
                [item.position_x + item.size_x, item.position_y],  # 右下坐标
                [item.position_x + item.size_x, item.position_y + item.size_y],  # 右上坐标
                [item.position_x, item.position_y + item.size_y]]  # 左上坐标
    return position


def get_line_position(position, line_x, line_y):  # position 每个点的坐标， line_size 绞线这个pdf对象的长和宽[X，Y]

    position1 = [[position[0][0] - line_x, position[0][1]],
                 [position[0][0] - line_x, position[0][1] + line_y]]
    position2 = [[position[0][0], position[0][1] - line_x],
                 [position[0][0] + line_y, position[0][1] - line_x]]
    position3 = [[position[1][0], position[1][1] - line_x],
                 [position[1][0] - line_y, position[1][1] - line_x]]
    position4 = [[position[1][0] + line_x, position[0][1]],
                 [position[1][0] + line_x, position[1][1] + line_y]]
    position5 = [[position[2][0] + line_x, position[2][1]],
                 [position[2][0] + line_x, position[2][1] - line_y]]
    position6 = [[position[2][0], position[2][1] + line_x],
                 [position[2][0] - line_y, position[2][1] + line_x]]
    position7 = [[position[3][0], position[3][1] + line_x],
                 [position[3][0] + line_y, position[3][1] + line_x]]
    position8 = [[position[3][0] - line_x, position[3][1]],
                 [position[3][0] - line_x, position[3][1] - line_y]]
    line = [position1, position2, position3, position4, position5, position6, position7, position8]

    return line


def determine_interner(item, line, determine):
    for i in range(8):
        if determine[i]:
            continue
        elif (((item.position_x + item.size_x) > line[i][0][0] > item.position_x) and (
                (item.position_y + item.size_y) > line[i][0][1] > item.position_y)) or (
                ((item.position_x + item.size_x) > line[i][1][0] > item.position_x) and (
                (item.position_y + item.size_y) > line[i][1][1] > item.position_y)):
            determine[i] = True


def find_all_class(starttime, endtime, conn, num):
    sql = f" SELECT  specsPaper,amount,filePath,productName FROM t_plate_order WHERE  specsPaper!='' and filePath != '' AND scheduleTime between {starttime} and {endtime} order by scheduleTime,orderTime "
    df = pd.read_sql(sql, con=conn)
    # if len(df) > num:
    #     n = num
    # else:
    n = len(df)
    character = []
    for i in range(n):
        if df.loc[i].filePath.endswith(('.pdf', '.PDF')):
            if df["productName"][i] == '合版名片' and (df["specsPaper"][i] == '单Y' or df["specsPaper"][i] == '单T'):
                if ['"' + str(df["amount"][i]) + '"', '"' + str(df["specsPaper"][i]) + '"', False, 1] not in character:
                    character.append(['"' + str(df["amount"][i]) + '"', '"' + str(df["specsPaper"][i]) + '"', False, 1])
                    continue
            elif df["productName"][i] == '合版名片':
                if ['"' + str(df["amount"][i]) + '"', '"' + str(df["specsPaper"][i]) + '"', True, 1] not in character:
                    character.append(['"' + str(df["amount"][i]) + '"', '"' + str(df["specsPaper"][i]) + '"', True, 1])
            elif df["productName"][i] == '合版单页':
                if ['"' + str(df["amount"][i]) + '"', '"' + str(df["specsPaper"][i]) + '"', True, 0] not in character:
                    character.append(['"' + str(df["amount"][i]) + '"', '"' + str(df["specsPaper"][i]) + '"', True, 0])
    return character


def draw_pdf3(mu, items, package, writepath, order, wires, duplex_print):
    output = PdfFileWriter()
    new_page = PageObject.createBlankPage(None, order[0].plate_size[0] * 2.836, order[0].plate_size[1] * 2.836)
    new_page1 = PageObject.createBlankPage(None, order[0].plate_size[0] * 2.836, order[0].plate_size[1] * 2.836)
    max_high = package.max_high
    seam = order[1].seam * 2.83
    left_seam = (order[0].plate_size[0] - order[1].effective_size[0]) * 2.83 / 2
    if max_high == 0:
        max_high = package.start

    for i in range(len(items)):
        if items[i].location not in mu.used_item:
            mu.used_item.append(items[i].location)

        input1 = PdfFileReader(items[i].location, strict=False)

        mu.sinOut.emit(f"写入第{mu.wi}个页面")
        mu.wi += 1

        if duplex_print:
            page1 = input1.getPage(items[i].page)
            page2 = input1.getPage(items[i].page + 1)
            if order[0].duplex_print_type == 1:
                if items[i].rotate:
                    new_page.mergeRotatedTranslatedPage(page1,
                                                        90,
                                                        left_seam + items[i].position_x + float(
                                                            page1.mediaBox.upperRight[1]),
                                                        seam + items[i].position_y)
                    new_page1.mergeRotatedTranslatedPage(page2,
                                                         270,
                                                         left_seam + items[i].position_x,
                                                         seam + package.size_y - items[i].position_y - (
                                                                 package.size_y - max_high) - items[i].size_y + float(
                                                             page2.mediaBox.upperRight[0]))

                else:

                    new_page.mergeRotatedTranslatedPage(page1,
                                                        0,
                                                        left_seam + items[i].position_x,
                                                        seam + items[i].position_y)
                    new_page1.mergeRotatedTranslatedPage(page2,
                                                         180,
                                                         left_seam + items[i].position_x + float(
                                                             page2.mediaBox.upperRight[0]),
                                                         seam + package.size_y - items[i].position_y - (
                                                                 package.size_y - max_high) - items[i].size_y + float(
                                                             page2.mediaBox.upperRight[1]))


            else:
                if items[i].rotate:
                    new_page.mergeRotatedTranslatedPage(page1,
                                                        90,
                                                        left_seam + items[i].position_x + float(
                                                            page1.mediaBox.upperRight[1]),
                                                        seam + items[i].position_y)
                    new_page1.mergeRotatedTranslatedPage(page2,
                                                         270,
                                                         left_seam + package.size_x - items[i].position_x - items[
                                                             i].size_x,
                                                         seam + items[i].position_y +
                                                         float(page2.mediaBox.upperRight[0]))

                else:

                    new_page.mergeRotatedTranslatedPage(page1,
                                                        0,
                                                        left_seam + items[i].position_x,
                                                        seam + items[i].position_y)
                    new_page1.mergeRotatedTranslatedPage(page2,
                                                         180,
                                                         left_seam + package.size_x - items[i].position_x - items[
                                                             i].size_x +
                                                         float(page2.mediaBox.upperRight[0]),
                                                         seam + items[i].position_y + float(
                                                             page2.mediaBox.upperRight[1]))



        else:  # 如果是单面打印
            page1 = input1.getPage(items[i].page)
            if items[i].rotate:
                new_page.mergeRotatedTranslatedPage(page1,
                                                    90,
                                                    left_seam + items[i].position_x + float(
                                                        page1.mediaBox.upperRight[1]),
                                                    seam + items[i].position_y)
            else:
                new_page.mergeRotatedTranslatedPage(page1,
                                                    0,
                                                    left_seam + items[i].position_x,
                                                    seam + items[i].position_y)

    if duplex_print:
        if order[0].duplex_print_type == 1:
            mu.sinOut.emit(f"正在绘制绞线!")
            new_page_line = PageObject.createBlankPage(None, package.size_x, package.size_y)  # 创建一个绞线pdf
            new_page_line1 = PageObject.createBlankPage(None, package.size_x, package.size_y)  # 创建背面一个绞线pdf
            input1 = PdfFileReader(open("line.pdf", "rb"), strict=False)
            input2 = PdfFileReader(open("midline.pdf", "rb"), strict=False)
            line = input1.getPage(0)
            midline = input2.getPage(0)
            for i in range(len(wires)):
                if wires[i].rotate:
                    new_page_line.mergeRotatedTranslatedPage(line,
                                                             90,
                                                             left_seam + wires[i].position_x + float(
                                                                 line.mediaBox.upperRight[1]),
                                                             seam + wires[i].position_y)
                    new_page_line1.mergeRotatedTranslatedPage(line,
                                                              90,
                                                              left_seam + wires[i].position_x + float(
                                                                  line.mediaBox.upperRight[1]),
                                                              seam + package.size_y - wires[
                                                                  i].position_y - (package.size_y - max_high) -
                                                              line.mediaBox.upperRight[0])

                else:
                    new_page_line.mergeRotatedTranslatedPage(line,
                                                             0,
                                                             left_seam + wires[i].position_x,
                                                             seam + wires[i].position_y)
                    new_page_line1.mergeRotatedTranslatedPage(line,
                                                              0,
                                                              left_seam + wires[i].position_x,
                                                              left_seam + package.size_y - wires[i].position_y - (
                                                                      package.size_y - max_high) -
                                                              line.mediaBox.upperRight[1])
            new_page_line1.mergeRotatedTranslatedPage(midline,
                                                      0,
                                                      (order[0].plate_size[0] / 2 - 5) * 2.83,
                                                      seam - 3 * 2.83)
            new_page_line1.mergeRotatedTranslatedPage(midline,
                                                      0,
                                                      (order[0].plate_size[0] / 2 - 5) * 2.83,
                                                      seam + order[1].effective_size[1] * 2.83)
            new_page_line1.mergeRotatedTranslatedPage(midline,
                                                      90,
                                                      left_seam,
                                                      seam + (order[1].effective_size[1] / 2 - 5) * 2.83)
            new_page_line1.mergeRotatedTranslatedPage(midline,
                                                      90,
                                                      left_seam + (order[1].effective_size[0] + 3) * 2.83,
                                                      seam + (order[1].effective_size[1] / 2 - 5) * 2.83)
            new_page_line.mergeRotatedTranslatedPage(midline,
                                                     0,
                                                     (order[0].plate_size[0] / 2 - 5) * 2.83,
                                                     seam - 3 * 2.83)
            new_page_line.mergeRotatedTranslatedPage(midline,
                                                     0,
                                                     (order[0].plate_size[0] / 2 - 5) * 2.83,
                                                     seam + order[1].effective_size[1] * 2.83)
            new_page_line.mergeRotatedTranslatedPage(midline,
                                                     90,
                                                     left_seam,
                                                     seam + (order[1].effective_size[1] / 2 - 5) * 2.83)
            new_page_line.mergeRotatedTranslatedPage(midline,
                                                     90,
                                                     left_seam + (order[1].effective_size[0] + 3) * 2.83,
                                                     seam + (order[1].effective_size[1] / 2 - 5) * 2.83)
        else:
            mu.sinOut.emit(f"正在绘制绞线!")
            new_page_line = PageObject.createBlankPage(None, package.size_x, package.size_y)  # 创建一个绞线pdf
            new_page_line1 = PageObject.createBlankPage(None, package.size_x, package.size_y)  # 创建背面一个绞线pdf
            input1 = PdfFileReader(open("line.pdf", "rb"), strict=False)
            input2 = PdfFileReader(open("midline.pdf", "rb"), strict=False)
            line = input1.getPage(0)
            midline = input2.getPage(0)
            for i in range(len(wires)):
                if wires[i].rotate:
                    new_page_line.mergeRotatedTranslatedPage(line,
                                                             90,
                                                             left_seam + wires[i].position_x + float(
                                                                 line.mediaBox.upperRight[1]),
                                                             seam + wires[i].position_y)
                    new_page_line1.mergeRotatedTranslatedPage(line,
                                                              90,
                                                              left_seam + package.size_x - wires[i].position_x,
                                                              seam + wires[i].position_y)

                else:
                    new_page_line.mergeRotatedTranslatedPage(line,
                                                             0,
                                                             left_seam + wires[i].position_x,
                                                             seam + wires[i].position_y)
                    new_page_line1.mergeRotatedTranslatedPage(line,
                                                              0,
                                                              left_seam + package.size_x - wires[i].position_x - float(
                                                                  line.mediaBox.upperRight[0]),
                                                              seam + wires[i].position_y)
            new_page_line1.mergeRotatedTranslatedPage(midline,
                                                      0,
                                                      (order[0].plate_size[0] / 2 - 5) * 2.83,
                                                      seam - 3 * 2.83)
            new_page_line1.mergeRotatedTranslatedPage(midline,
                                                      0,
                                                      (order[0].plate_size[0] / 2 - 5) * 2.83,
                                                      seam + order[1].effective_size[1] * 2.83)
            new_page_line1.mergeRotatedTranslatedPage(midline,
                                                      90,
                                                      left_seam,
                                                      seam + (order[1].effective_size[1] / 2 - 5) * 2.83)
            new_page_line1.mergeRotatedTranslatedPage(midline,
                                                      90,
                                                      left_seam + (order[1].effective_size[0] + 3) * 2.83,
                                                      seam + (order[1].effective_size[1] / 2 - 5) * 2.83)
            new_page_line.mergeRotatedTranslatedPage(midline,
                                                     0,
                                                     (order[0].plate_size[0] / 2 - 5) * 2.83,
                                                     seam - 3 * 2.83)
            new_page_line.mergeRotatedTranslatedPage(midline,
                                                     0,
                                                     (order[0].plate_size[0] / 2 - 5) * 2.83,
                                                     seam + order[1].effective_size[1] * 2.83)
            new_page_line.mergeRotatedTranslatedPage(midline,
                                                     90,
                                                     left_seam,
                                                     seam + (order[1].effective_size[1] / 2 - 5) * 2.83)
            new_page_line.mergeRotatedTranslatedPage(midline,
                                                     90,
                                                     left_seam + (order[1].effective_size[0] + 3) * 2.83,
                                                     seam + (order[1].effective_size[1] / 2 - 5) * 2.83)

    else:
        mu.sinOut.emit(f"正在绘制绞线!")
        new_page_line = PageObject.createBlankPage(None, package.size_x, package.size_y)  # 创建一个绞线pdf
        new_page_line1 = PageObject.createBlankPage(None, package.size_x, package.size_y)  # 创建背面一个绞线pdf
        input1 = PdfFileReader(open("line.pdf", "rb"), strict=False)
        input2 = PdfFileReader(open("midline.pdf", "rb"), strict=False)
        line = input1.getPage(0)
        midline = input2.getPage(0)
        for i in range(len(wires)):
            if wires[i].rotate:
                new_page_line.mergeRotatedTranslatedPage(line,
                                                         90,
                                                         left_seam + wires[i].position_x + float(
                                                             line.mediaBox.upperRight[1]),
                                                         seam + wires[i].position_y)
                new_page_line1.mergeRotatedTranslatedPage(line,
                                                          90,
                                                          left_seam + wires[i].position_x + float(
                                                              line.mediaBox.upperRight[1]),
                                                          seam + wires[i].position_y)

            else:
                new_page_line.mergeRotatedTranslatedPage(line,
                                                         0,
                                                         left_seam + wires[i].position_x,
                                                         seam + wires[i].position_y)
        new_page_line.mergeRotatedTranslatedPage(midline,
                                                 0,
                                                 (order[0].plate_size[0] / 2 - 5) * 2.83,
                                                 seam - 3 * 2.83)
        new_page_line.mergeRotatedTranslatedPage(midline,
                                                 0,
                                                 (order[0].plate_size[0] / 2 - 5) * 2.83,
                                                 seam + order[1].effective_size[1] * 2.83)
        new_page_line.mergeRotatedTranslatedPage(midline,
                                                 90,
                                                 left_seam,
                                                 seam + (order[1].effective_size[1] / 2 - 5) * 2.83)
        new_page_line.mergeRotatedTranslatedPage(midline,
                                                 90,
                                                 left_seam + (order[1].effective_size[0] + 3) * 2.83,
                                                 seam + (order[1].effective_size[1] / 2 - 5) * 2.83)
    # Write file
    i = items[0].index

    if duplex_print:
        new_page.mergeTranslatedPage(new_page_line,
                                     0,
                                     0
                                     )
        new_page1.mergeTranslatedPage(new_page_line1,
                                      0,
                                      0
                                      )
        new_page.scaleBy(order[1].scale)
        new_page1.scaleBy(order[1].scale)
        output.addPage(new_page)
        output.addPage(new_page1)
    else:
        new_page.mergeTranslatedPage(new_page_line,
                                     0,
                                     0
                                     )

        new_page.scaleBy(order[1].scale)
        output.addPage(new_page)
    machine = order[0].name
    plate_mod = order[1].mod_num

    output.write(open(writepath + "\\" + str(i) + machine + str(plate_mod) + "模.pdf", "wb"))
    print()


def collect_same_order(items):
    used_item = []
    a = []
    for i in range(len(items)):
        if i in used_item:
            continue
        used_item.append(i)
        same_order = [items[i]]
        for j in range(i, len(items)):
            if j in used_item:
                continue
            if items[i].location == items[j].location:
                same_order.append(items[j])
                used_item.append(j)
        same_order.sort(key=lambda x: x.page)
        a.append(same_order)
    return a


def select_charater(same_order, duplex_print,package,packages):
    if duplex_print:
        package_id = []
        position = []
        rotate = []
        page = 0
        size = []

        for i in range(len(same_order)):
            max_high = packages[same_order[i].index].max_high
            package_id += [same_order[i].index] * 2
            if package[same_order[i].index][1].plate_type == 0:
                position += [[same_order[i].position_x/2.838, same_order[i].position_y/2.838]]
                position += [[package[same_order[i].index][1].effective_size[0]-same_order[i].size_x/2.838-same_order[i].position_x / 2.838 , same_order[i].position_y / 2.838 ]]
            else:
                position += [[same_order[i].position_x / 2.838, same_order[i].position_y / 2.838 ]]
                position += [[same_order[i].position_x / 2.838 , package[same_order[i].index][1].effective_size[1]-same_order[i].position_y / 2.838-(package[same_order[i].index][1].effective_size[1]-max_high) - same_order[i].size_y/2.838]]

            rotate += [same_order[i].rotate] * 2
            page += 2
            size += [[same_order[i].size_x/2.83, same_order[i].size_y/2.83]] * 2

    return package_id, position, rotate, page, size

def select_line_charater(total_wires,duplex_print,used_package,packages):
    package_id = []
    position = []
    rotate = []
    page = 0
    size = []
    for i in range(len(total_wires)):
        max_high = packages[i].max_high
        if duplex_print:
            package_id += [i] * len(total_wires[i])*2
            for j in range(len(total_wires[i])):
                position.append([total_wires[i][j].position_x/2.838, total_wires[i][j].position_y/2.838])
                if used_package[i][1].plate_type == 0:
                    position.append([used_package[i][1].effective_size[0]-3-total_wires[i][j].position_x/2.838, total_wires[i][j].position_y/2.838])
                else:
                    position.append([total_wires[i][j].position_x/2.838, used_package[i][1].effective_size[1]-(used_package[i][1].effective_size[1]-max_high/2.838) - 3- total_wires[i][j].position_y/2.838])
                rotate += [total_wires[i][j].rotate]*2
                page += 2
                if total_wires[i][j].rotate:
                    size+= [[6, 8]]*2
                else:
                    size+= [[8, 6]]*2
        else:
            package_id += [i]*len(total_wires[i])
            for j in range(len(total_wires[i])):
                position .append([total_wires[i][j].position_x,total_wires[i][j].position_y])
                rotate.append(total_wires[i][j].rotate)
                page += 1
                if total_wires[i][j].rotate:
                    size.append([6,8])
                else:
                    size.append([8,6])
    return package_id,position,rotate,page,size

def select_midline_charater(used_package,duplex_print):
    package_id = []
    position = []
    rotate = []
    page = 0
    size = []
    for i in range(len(used_package)):
        scale = used_package[i][1].scale
        if duplex_print:
            package = used_package[i]
            left_seam = (package[0].plate_size[0] - package[1].effective_size[0])/2
            package_id += [i]*8
            position+=[[(package[1].effective_size[0]/2-5)/scale, -3]]*2
            position += [[(package[1].effective_size[0] / 2 - 5)/scale, int(package[1].effective_size[1])]] * 2
            position += [[(-3)/scale,(package[1].effective_size[1]/2 -5)]] * 2
            position += [[int(package[1].effective_size[0])/scale,(package[1].effective_size[1]/2 -5)]] * 2
            rotate += [False,False,False,False,True,True,True,True]
            page += 8
            size += [[10,3],[10,3],[10,3],[10,3],[3,10],[3,10],[3,10],[3,10]]
        else:
            package = used_package[i]
            left_seam = (package[0].plate_size[0] - package[1].effective_size[0]) / 2
            package_id += [i] * 4
            position += [[(package[0].plate_size[0]/ 2 - 5) / scale, package[1].seam - 3]]
            position += [[(package[0].plate_size[0]/ 2 - 5) / scale, package[1].seam + package[1].effective_size[1]]]
            position += [[(left_seam) / scale, package[1].seam + (package[1].effective_size[1] / 2 - 5)]]
            position += [[(left_seam + package[1].effective_size[1] + 3) / scale,
                          package[1].seam + (package[1].effective_size[1] / 2 - 5)]]
            rotate += [False, False, True, True]
            page += 4
            size += [[10, 3], [10, 3], [3, 10],  [3, 10]]
    return package_id, position, rotate, page, size



def create_pdf(b, items, order, duplex_print, packages):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y%m%d")
    used_item = []
    used_package = []
    items_in_same_package = []
    line_size = [8 * 2.83, 6*2.83]
    total_wires = []
    for i in range(b):  # 得到所有需要画的item的集和
        a = list(filter(lambda x: x.index == i, items))
        used_item = used_item + a
        items_in_same_package.append(a)
        used_package.append(order[i])
    all_plating = {"items": {}, "packages": {},"gripper":{}}
    plate_size = str(used_package[i][1].effective_size[0])+"*"+str(used_package[i][1].effective_size[1])
    all_plating["gripper"]["name"] = "[版一]"+used_package[i][1].jobNoPrefix + formatted_date + used_package[i][1].corename+"板材"+plate_size
    same_order = collect_same_order(used_item)

    for i in range(len(same_order)):  # 生成item
        item_name = "item" + str(i)
        all_plating["items"][item_name] = {}
        package_id, position, rotate, page, size = select_charater(same_order[i], duplex_print,used_package,packages)
        all_plating["items"][item_name]["package_id"] = package_id
        all_plating["items"][item_name]["location"] = same_order[i][0].location
        all_plating["items"][item_name]["position"] = position
        all_plating["items"][item_name]["rotate"] = rotate
        all_plating["items"][item_name]["page"] = page
        all_plating["items"][item_name]["is_rep"] = False
        all_plating["items"][item_name]["size"] = size

    for i in range(len(used_package)):
        package_name = "package" + str(i)
        scale = used_package[i][1].scale
        left_seam = int(used_package[i][0].plate_size[0]-scale*used_package[i][1].effective_size[0])/2
        wires = find_line_position(items_in_same_package[i], line_size)
        total_wires.append(wires)
        all_plating["packages"][package_name] = {}
        all_plating["packages"][package_name]["id"] = list([i])
        all_plating["packages"][package_name]["size"] = list([int(used_package[i][0].plate_size[0]), int(used_package[i][0].plate_size[1])])
        all_plating["packages"][package_name]["area_size"] = list([int(used_package[i][1].effective_size[0]), int(used_package[i][1].effective_size[1])])
        all_plating["packages"][package_name]["area_scale"] = list([used_package[i][1].scale, 1])
        all_plating["packages"][package_name]["area_loc"] = list([left_seam, used_package[i][1].seam])
        all_plating["packages"][package_name]["duplex_print"] = duplex_print
        all_plating["packages"][package_name]["output_file_name"] = "F:\\pythonWorkPlace\\mycode\\gui\\gui\\result\\"+used_package[i][0].name+str(used_package[i][1].mod_num)+".pdf"

    package_id,position,rotate,page,size = select_line_charater(total_wires,duplex_print,used_package,packages)
    all_plating["items"]["line"] = {}
    all_plating["items"]["line"]["package_id"] = package_id
    all_plating["items"]["line"]["location"] = "F:\\pythonWorkPlace\\mycode\\gui\\gui\\line.pdf"
    all_plating["items"]["line"]["position"] = position
    all_plating["items"]["line"]["rotate"] = rotate
    all_plating["items"]["line"]["page"] = page
    all_plating["items"]["line"]["is_rep"] = True
    all_plating["items"]["line"]["size"] = size

    package_id,position,rotate,page,size = select_midline_charater(used_package,duplex_print)
    all_plating["items"]["mid_line"] = {}
    all_plating["items"]["mid_line"]["package_id"] = package_id
    all_plating["items"]["mid_line"]["location"] = "F:\\pythonWorkPlace\\mycode\\gui\\gui\\midline.pdf"
    all_plating["items"]["mid_line"]["position"] = position
    all_plating["items"]["mid_line"]["rotate"] = rotate
    all_plating["items"]["mid_line"]["page"] = page
    all_plating["items"]["mid_line"]["is_rep"] = True
    all_plating["items"]["mid_line"]["size"] = size

    return all_plating


def del_file(path_data):
    for i in os.listdir(path_data):  # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "\\" + i  # 当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:  # os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
        else:
            del_file(file_data)
            os.rmdir(file_data)


def read_package(path):
    files = [f for f in os.listdir(path)]
    files = list(filter(lambda f: f.endswith(('.pdf', '.PDF')), files))
    end_files = []
    for file in files:
        a = os.path.join(path, file)
        end_files.append(a)

    return end_files


def get_order_by_mod(printers, plate_type, total_mod_num, amount):  # plate_type 订单要求的版类型，total_mod_num 总模数,amount 印刷数量
    plate_order_list = list()
    # 寻找最适合的模数大版
    # 获取所有可用的负荷类型的大版
    avaliable_printers_plates = []
    for pt in printers:  # 筛选可用的大版
        plts = []
        for plt in pt.plates:
            if plt.plate_type == plate_type:
                plts.append(plt)
        avaliable_printers_plates.append(plts)

    remain_mod_num = int(2 * total_mod_num)
    while (remain_mod_num > 0):
        min_prt, prop_plate, use_plate_num = find_prop_printer_and_plate_within_avaliable(printers,
                                                                                          avaliable_printers_plates,
                                                                                          remain_mod_num)
        if min_prt is None:
            return []
        plate_order_list.append([min_prt, prop_plate])

        remain_mod_num = remain_mod_num - prop_plate.mod_num  # 计算剩余的模数
        min_prt.plates_remain = min_prt.plates_remain - 1
        min_prt.work_time = min_prt.work_time + amount
    return plate_order_list

    # return new_order


def find_prop_printer_and_plate_within_avaliable(printers, avaliable_printers_plates,
                                                 total_mod_num):  # avaliable_printers_plates,二维数组表示[[]]第一维表示各个打印机，第二维里面存的是对应打印机里可以打印订单的版的对象
    min_time = 10000000000  # 最少工作时间
    min_mod = 1000  # 最少模数剩余
    max_remain = 0  # 最大剩余耗材
    use_plate_num = 0
    min_ava_mod = 10000
    # 综合权重
    min_prt = None
    prop_plate = None
    for prt in printers:  # 选择最空闲的印刷机
        prtx = prt
        idx = printers.index(prt)
        if avaliable_printers_plates[idx] != []:  # 找到印刷机里
            if (min_time > prtx.work_time) and prtx.sate:
                for plt in avaliable_printers_plates[idx]:  # 判断是否有模数接近的
                    if total_mod_num % plt.mod_num <= min_mod:
                        if total_mod_num <= plt.mod_num:
                            if min_ava_mod > plt.mod_num:
                                min_time = prtx.work_time
                                min_prt = prt
                                prop_plate = plt
                                # max_remain = plt.remain
                                min_mod = total_mod_num % plt.mod_num
                                use_plate_num = plt.mod_num  # 使用的模数
                                min_ava_mod = plt.mod_num
                        elif prt.plates_remain > max_remain:
                            min_time = prtx.work_time
                            min_prt = prt
                            prop_plate = plt
                            max_remain = prt.plates_remain
                            min_mod = total_mod_num % plt.mod_num
                            use_plate_num = plt.mod_num  # 使用的模数
    return min_prt, prop_plate, use_plate_num


def get_min_model(plates):
    min_mode = pd.Series()

    for plate in plates:
        if plate.plate_type not in min_mode:
            a = pd.Series(plate.mod_num, index=[plate.plate_type])
            min_mode = pd.concat([min_mode, a], axis=0, ignore_index=True)
        else:
            if plate.mod_num < min_mode[plate.plate_type]:
                min_mode[plate.plate_type] = plate.mod_num

    return min_mode


def get_int(amount):
    amount = amount.replace("'", "").replace('"', '')
    a = int(amount)
    return a


def get_all_model(characters, readpath, conn, starttime, endtime):
    model = []
    for character in characters:
        _, a = read_sql(character[1], character[0], readpath, conn, 0, starttime, endtime)
        model.append(a)
    return model


def draw_bins(squares, bin_size_x, bin_size_y, num):
    step = 1
    im_dim_x = (bin_size_x + 2) * step
    im_dim_y = ((bin_size_y + 1) + 1) * step
    im = Image.new('RGB', (im_dim_x, im_dim_y), (256, 256, 256))
    draw = ImageDraw.Draw(im)
    number_of_drawn_bins = 0
    bin_pos_x = step
    bin_pos_y = step + (number_of_drawn_bins * ((bin_size_y + 1) * step))
    draw.rectangle((bin_pos_x, bin_pos_y, bin_pos_x + bin_size_x * step, bin_pos_y + bin_size_y * step),
                   fill=(255, 255, 255), outline=(0, 0, 26))
    draw_squares(squares, step, draw, bin_pos_x, bin_pos_y)  # 画出处于这个箱子中的盒子

    im.save('./result/bins' + str(num) + '.jpg', quality=95)


def draw_squares(squares_for_bin, step, draw, bin_pos_x, bin_pos_y):
    for square in squares_for_bin:
        lc_x = bin_pos_x + square.position_x * step
        lc_y = bin_pos_y + square.position_y * step
        rc_y = lc_y + square.size_y * step
        rc_x = lc_x + square.size_x * step
        # Font selection from the downloaded file
        myFont = ImageFont.truetype("C:\\WINDOWS\\Fonts\\Arial.TTF", 100)

        # Decide the text location, color and font
        c = str(square.color_cluster)
        R = int(square.rgb[0])
        G = int(square.rgb[1])
        B = int(square.rgb[2])
        draw.rectangle((lc_x, lc_y, rc_x, rc_y), fill=(R, G, B), outline=(0, 0, 0))
        draw.text((lc_x, lc_y + 10), c, fill='red', font=myFont)


def merge_character(characters, plates, starttime, endtime, readpath, conn):  # 这里默认characters是按照纸张类型分类，并按照数量由大到小进行排列
    all_the_model = get_all_model(characters, readpath, conn, starttime, endtime)
    merged = []
    for i in range(len(all_the_model)):
        if all_the_model[i] == 0:
            merged.append(i)
    min_mod = get_min_model(plates)  # 获得每个版面类型中的最小模数
    new_character_common = []
    new_character = []
    new_model_common = []
    new_model = []
    num_of_amount_common = []  # 用于记录同一类别合并后的订单张数
    num_of_amount = []
    specs_paper = characters[0][1]
    for i in range(len(characters)):  # 对存在的订单类别进行循环
        if i in merged:
            continue
        if specs_paper != characters[i][1]:  # 如果当前类别已经遍历完，换一下类别
            specs_paper = characters[i][1]
            for h in range(len(new_character_common)):
                new_character.append(new_character_common[h])
                num_of_amount.append(num_of_amount_common[h])
                new_model.append(new_model_common[h])
            new_character_common = []
            num_of_amount_common = []  # 用于记录同一类别合并后的订单张数
            new_model_common = []
        total_model = all_the_model[i]
        amount = get_int(characters[i][0])  # 用于记录当前所需要的订单张数
        j = i
        a = [characters[i]]
        merged.append(i)
        while total_model < min_mod[characters[i][3]] and j < len(characters) and specs_paper == characters[j][
            1]:  # 当总的模数大于版面最大模数时或者这个类别遍历完后合并停止
            if j in merged:
                j += 1
                continue
            multiple_of_order = amount / get_int(characters[j][0])  # 后面的订单是当前订单的倍数
            if multiple_of_order > 1 and amount % get_int(characters[j][0]) == 0:  # 寻找订单倍数可以整除的可合并订单
                tm = all_the_model[j]
                total_model = multiple_of_order * total_model + tm  # 合并后的模数
                amount = get_int(characters[j][0])  # 合并后所需要打印的纸张数
                a.append(characters[j])
                merged.append(j)
            j += 1
        if total_model < min_mod[characters[i][3]] and amount != get_int(
                characters[i][0]):  # 如果循环完成后模数任然不够,并且已经合并后（如果没合并，没有向前循环的必要，因为全都循环过了），在向前循环一次（先在未完成拼版的订单中循环）
            for k in range(j - 1, i, -1):
                if k in merged:
                    continue

                multiple_of_order = get_int(characters[k][0]) / amount  # 后面的订单是当前订单的倍数
                if multiple_of_order > 1 and get_int(characters[k][0]) % amount == 0:  # 寻找订单倍数可以整除的可合并订单
                    tm = all_the_model[k]
                    if tm > min_mod[characters[i][3]]:  # 如果多的那个纸张数大于最小模数，就不考虑拆分，因为这样最少都会会拆分成两个，会得不偿失
                        continue
                    total_model = multiple_of_order * tm + total_model  # 合并后的模数
                    a.append(characters[k])
                    merged.append(k)
                if total_model > min_mod[characters[i][3]]:
                    break
        new_model_common.append(total_model)
        new_character_common.append(a)
        num_of_amount_common.append(amount)

    for h in range(len(new_character_common)):
        new_character.append(new_character_common[h])
        num_of_amount.append(num_of_amount_common[h])
        new_model.append(new_model_common[h])

    return new_character, num_of_amount, new_model


class makeup(QThread):
    sinOut = pyqtSignal(str)
    qmuit = QMutex()

    def __init__(self, windows, conn, starttime, endtime, readpath, writepath, num, printers, plates, character,
                 used_item):
        super(makeup, self).__init__()

        self.readpath = readpath
        self.writepath = writepath
        self.num = num
        self.printers = printers
        self.plates = plates
        self.character = character
        self.starttime = starttime
        self.endtime = endtime

        self.windows = windows
        self.conn = conn
        self.used_item = used_item

    def make(self, characters, base_amount, model, readpath, writepath, conn):

        items = []
        total_location = []
        copy = []
        json_data = self.windows.json_data
        spacepaper = characters[0][1]
        duplex_print = characters[0][2]
        plate_type = characters[0][3]
        color_location = []
        for i in range(len(characters)):
            character = []
            sql_amount = characters[i][0]
            sql_amount = sql_amount.replace('"', '')
            sql_amount = sql_amount.replace("'", '')
            amount = int(sql_amount)
            copy.append(int(amount / base_amount))  # 将倍数放入
            location, _ = read_sql(spacepaper, sql_amount, readpath, conn, self.num, self.starttime, self.endtime)
            if len(location) == 0:
                self.sinOut.emit(f"克重：{spacepaper}，数量:{sql_amount}没有这个订单")
                return
            for j in range(len(location)):
                color_location.append(location[j])
            total_location.append(location)
            character.append([spacepaper, sql_amount])
            self.sinOut.emit(f"克重：{spacepaper}，数量:{sql_amount}，总共有{len(location)}个订单需要读取")
        if len(character) > 1:
            for i in range(len(character)):
                spacepaper = character[i][0]
                sql_amount = character[i][1]
                if i == len(character) - 1:
                    self.sinOut.emit(f"克重：{spacepaper}，数量:{sql_amount}结合为一类，其中打印数量为{base_amount}")
                self.sinOut.emit(f"克重：{spacepaper}，数量:{sql_amount}与")

        color_label, rgbs = classify(color_location)
        if duplex_print:
            sequence = 0
            color_id = 0
            for i in range(len(total_location)):
                for k in range(len(total_location[i])):
                    reader = PdfFileReader(open(total_location[i][k], "rb"), strict=False)
                    num_of_page = reader.getNumPages()
                    label = color_label[color_id]
                    rgb = rgbs[color_id]
                    color_id += 1
                    self.sinOut.emit(f"正在读取第{i + 1}个订单")
                    if num_of_page % 2 == 1:  # 如果Pdf文件中的页数为奇数
                        num_of_page -= 1
                    for j in range(0, num_of_page, 2):  # 对pdf对象创建item对象
                        if j == 0:
                            c = item(total_location[i][k])
                            c.get_size()
                            c.get_square()
                            c.sequence = sequence
                            c.page = j
                            c.color_cluster = label
                            c.rgb = rgb
                            size_x = c.size_x
                            size_y = c.size_y
                            for h in range(copy[i]):  # 复制多少个
                                a = c.copy_item()
                                a.sequence = sequence
                                items.append(a)
                                sequence += 1
                        else:
                            c = item(total_location[i][k])
                            c.size_x = size_x
                            c.size_y = size_y
                            c.page = j
                            c.rgb = rgb
                            c.color_cluster = label
                            for h in range(copy[i]):
                                a = c.copy_item()
                                a.sequence = sequence
                                items.append(a)
                                sequence += 1
        else:
            sequence = 0
            color_id = 0
            for i in range(len(total_location)):
                for k in range(len(total_location[i])):
                    reader = PdfFileReader(open(total_location[i][k], "rb"), strict=False)
                    num_of_page = reader.getNumPages()
                    self.sinOut.emit(f"正在读取第{i + 1}个订单")
                    label = color_label[color_id]
                    rgb = rgbs[color_id]
                    color_id += 1
                    for j in range(num_of_page):
                        if j == 0:
                            c = item(total_location[i][k])
                            c.get_size()
                            c.get_square()
                            c.page = j
                            c.color_cluster = label
                            c.rgb = rgb
                            size_x = c.size_x
                            size_y = c.size_y
                            for h in range(copy[i]):
                                a = c.copy_item()
                                a.sequence = sequence
                                items.append(a)
                                sequence += 1
                        else:
                            c = item(total_location[i][k])
                            c.size_x = size_x
                            c.size_y = size_y
                            c.color_cluster = label
                            c.rgb = rgb
                            c.page = j
                            for h in range(copy[i]):
                                a = c.copy_item()
                                a.sequence = sequence
                                items.append(a)
                                sequence += 1

        self.sinOut.emit(f"正在读取 克重：{spacepaper}，数量:{sql_amount}中订单颜色，并根据订单颜色对订单进行分类！")

        # TIME3 = time.perf_counter()
        # str_amount = sql_amount.replace('"', '')
        # tmp_amount = str_amount.replace("'", '')
        # amount = int(tmp_amount)

        order = get_order_by_mod(self.printers, plate_type, model, base_amount)
        if len(order) == 0:
            self.sinOut.emit(f"缺少能打印这种订单类型的打印机")
            return
        package_order = []
        for i in range(len(order)):
            package_order.append(order[i][1].effective_size)

        area = 0
        item_total = 0
        starting_number_of_bins = 0
        for i in range(len(items)):
            item_total += items[i].square
        while area <= item_total:
            area += package_order[starting_number_of_bins][0] * package_order[starting_number_of_bins][1] * 2.83 * 2.83
            starting_number_of_bins += 1

        generation_size = 50
        recombination = 0.8
        mutation = 0.5

        max_generations = 100
        stop_criterium = 1
        cut_in_y = True
        spacepaper = spacepaper.replace('"', '')
        label = spacepaper + '-' + str(base_amount)  # 当前创建的标签
        TIME4 = time.perf_counter()
        _, c, items, packages = use_genetics(self.sinOut, items, generation_size,
                                             recombination,
                                             mutation, max_generations, stop_criterium, package_order,
                                             cut_in_y, label)
        TIME5 = time.perf_counter()

        writepath = writepath + '\\' + label
        os.mkdir(writepath)
        items_in_one_package = []
        b = 0
        for i in range(len(items)):
            if items[i].index > b:
                b = items[i].index

        self.sinOut.emit(f"最终一共需要用到{b + 1}个大版，总共有{len(items)}个订单")
        self.wi = 1
        last_item = list(filter(lambda x: x.index == b, items))
        last_package_area = 0
        for i in range(len(last_item)):
            last_package_area += last_item[i].square
        if (last_package_area / (packages[b].size_x * packages[b].size_y)) >= 0.5:
            b += 1
        del_file('./result')
        self.sinOut.emit(f"开始调用coreldraw插件，进行拼版pdf写入")
        all_plate = create_pdf(b, items, order, duplex_print,packages)
        # json_data = json.dumps(all_plate)
        with open('plate.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(all_plate, indent=2, ensure_ascii=False))
        # json_data = str(json_data)
        result = subprocess.run(['CorelDrawPlating.exe'], capture_output=True, text=True)
        print(result.stdout)
        for i in range(b):
            a = list(filter(lambda x: x.index == i, items))
            # wires = find_line_position(a, line_size)
            # drfsdaw_pdf3(self, a, packages[i], writepath, order[i], wires, duplex_print)
            draw_bins(a, packages[i].size_x, packages[i].size_y, i)

        # work_time = []
        # remains = []
        # for prt in self.printers:
        #     work_time.append(prt.work_time)
        # for plt in self.plates:
        #     remains.append(plt.remain)
        # json_data["printer"]["work_time"] = work_time
        # json_data["plate"]["remain"] = remains
        # jso = json.dumps(json_data)
        # with open('jsondata.json', "w") as js:
        #     js.write(jso)

    def run(self):

        # character = find_all_class(self.starttime, self.endtime, self.conn, self.num)
        # sql = f" SELECT filePath FROM t_plate_order WHERE specsPaper= '' and amount = '25' and filePath != ''"
        # df = pd.read_sql(sql, con=conn)
        # a = read_sql("","25")
        del_file(self.writepath)
        # writepath = "/拼版结果" characters, plates,starttime,endtime,readpath,conn

        new_character, new_amount, new_model = merge_character(self.character, self.plates, self.starttime,
                                                               self.endtime, self.readpath,
                                                               self.conn)

        for i in range(len(new_character)):
            self.make(new_character[i], new_amount[i], new_model[i], self.readpath, self.writepath, self.conn,
                      )
        self.sinOut.emit(f"拼版结束，请在{self.writepath}查看拼版结果文件")
