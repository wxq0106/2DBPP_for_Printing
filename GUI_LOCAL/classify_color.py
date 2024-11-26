# WXQ
# 时间： $(DATE) $(TIME)
from cal_cmyk import  cal_rgb,get_dominant_color
import os
from sklearn.cluster import KMeans
import math
import pandas as pd
import pymysql



def read_sql(character1, character2, readpath, conn, num, starttime, endtime):
    cursor = conn.cursor()
    sql = f" SELECT filePath, moshu FROM t_plate_order WHERE specsPaper= {character1} and amount = {character2} and filePath != ''  AND specsPaper !='' AND scheduleTime between {starttime} and {endtime} order by scheduleTime,orderTime"
    df = pd.read_sql(sql, con=conn)
    # if len(df) > num:
    #     n = num
    # else:
    n = len(df)
    end_files = []
    total_model = 0
    for i in range(n):
        if df.loc[i].filePath.endswith(('.pdf', '.PDF')):
            a = df.loc[i].filePath.replace("订单文件/", "").replace("/", "\\")
            b = os.path.join(readpath, a)
            if os.path.exists(b):  # 判断文件存不存在
                end_files.append(b)
                total_model += int(df.loc[i].moshu)
            else:
                print(f"文件{b}不存在")

    return end_files, total_model


def read_package(path):
    files = [f for f in os.listdir(path)]
    files = list(filter(lambda f: f.endswith(('.pdf', '.PDF')), files))
    end_files = []
    for file in files:
        a = os.path.join(path, file)
        end_files.append(a)

    return end_files



def classify_rgb(pic_rgbs):
    cls = []
    # 标定的类别标准色
    pr = [255, 0, 0]
    pg = [0, 255, 0]
    pb = [0, 0, 255]
    pw = [255, 255, 255]
    pk = [0, 0, 0]

    psv_1 = [-1, 0, 1]
    psv_2 = [-1, 0, 0.5]
    psv_3 = [-1, 0, 0]
    psv0 = [0, 1, 1]
    psv1 = [60, 1, 0.7]
    psv2 = [120, 1, 0.5]
    psv3 = [180, 0.5, 1]
    psv4 = [240, 0.5, 1]
    psv5 = [300, 0.667, 0.75]
    psv6 = [61.8, 0.779, 0.643]
    psv7 = [251.1, 0.887, 0.918]
    psv8 = [134.9, 0.828, 0.675]
    psv9 = [49.5, 0.944, 0.941]
    psv10 = [283.7, 0.792, 0.897]
    psv11 = [14.3, 0.661, 0.931]
    psv12 = [56.9, 0.467, 0.998]
    psv13 = [162.4, 0.875, 0.795]
    psv14 = [248.3, 0.75, 0.597]
    psv15 = [240.5, 0.316, 0.721]
    # 类别数组
    hsv_pcls = [psv_1, psv_3, psv0, psv1, psv2, psv3, psv4, psv5, psv6, psv7, psv8, psv9, psv10, psv11, psv12, psv13,
                psv14, psv15]
    cls_ind = [0, 5, 1, 4, 2, 3, 3, 1, 4, 3, 2, 4, 1, 1, 4, 2, 3, 3]  # 0表示白，1表示红，2表示绿，3表示蓝，4表示黄，5表示黑,6表示灰
    # hsv_pcls=[psv_1,psv0,psv2,psv7,psv9]
    # hsv_pcls=[]
    # for pc in pcls:
    #    hsv_pcls.append(rgb2hsv(pc))

    for e in pic_rgbs:
        hsv = rgb2hsv(e)
        s = []  # 和各类别的距离
        for pc in hsv_pcls:
            s.append(HSVDIstance(hsv, pc))
        if hsv[1] <= 0.168 and 0.18 <= hsv[2] <= 0.97:
            cls.append(6)
        elif hsv[1] <= 0.12 and hsv[2] > 0.97:
            cls.append(0)
        elif hsv[2] < 0.18:
            cls.append(5)
        else:
            cls.append(cls_ind[s.index(min(s))])
    return cls


def rgb2hsv(rgb):
    r, g, b = [it / 255.0 for it in rgb]
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if (mx == mn):
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 0) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df / mx
    v = mx
    return h, s, v


def HSVDIstance(hsv1, hsv2):
    H1, S1, V1 = hsv1
    H2, S2, V2 = hsv2
    if H1 == -1:
        H1 = H2
    if H2 == -1:
        H2 = H1
    R = 100
    angle = 30
    h = R * math.cos(angle / 180 * math.pi)
    r = R * math.sin(angle / 100 * math.pi)
    x1 = r * V1 * S1 * math.cos(H1 / 180 * math.pi)
    y1 = r * V1 * S1 * math.sin(H1 / 180 * math.pi)
    z1 = h * (1 - V1)
    x2 = r * V2 * S2 * math.cos(H2 / 180 * math.pi)
    y2 = r * V2 * S2 * math.sin(H2 / 180 * math.pi)
    z2 = h * (1 - V2)
    dx = x1 - x2
    dy = y1 - y2
    dz = z1 - z2
    return math.sqrt(dx * dx + dy * dy + dz * dz)


# def classify_cmyks(cmyks):
#    cls = []
#    # 标定的类别
#    c = [100, 0, 0, 0]
#    m = [0, 100, 0, 0]
#    y = [0, 0, 100, 0]
#    k = [0, 0, 0, 100]
#    # 类别数组
#    pcls = [c, m, y, k]
#    for e in cmyks:
#        ne = math.sqrt(e[0] * e[0] + e[1] * e[1] + e[2] * e[2] + e[3] * e[3])  # 计算模长
#        s = []  # 和各类别的相似度
#        for pc in pcls:
#            s.append(pc[0] * e[0] + pc[1] * e[1] + pc[2] * e[2] + pc[3] * e[3] / (ne * 100))
#        cls.append(s.index(max(s)))
#    return cls


def classify(location):
    # paths=read_package(path)

    rgbs = []
    if len(location) < 4:
        labels = [1]*len(location)
        rgbs = [[0,0,0]]*len(location)
        return labels,rgbs

    for i in range(len(location)):
        a = get_dominant_color(location[i])
        rgbs.append(a)

    labels = classify_rgb(rgbs)
    locat = []
    # for i in range(len(items)):
    #     items[i].color_cluster = labels[i]
    #     if labels[i] == 1:
    #         locat.append(items[i].location)
    return labels,rgbs