#WXQ
#时间： $(DATE) $(TIME)
import cv2
from pdf2image import convert_from_path
import PyPDF3
import io
import numpy as np
import urllib
import colorsys

rgb_scale = 255
cmyk_scale = 100


def rgb_to_cmyk(r,g,b):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / float(rgb_scale)
    m = 1 - g / float(rgb_scale)
    y = 1 - b / float(rgb_scale)

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy)
    m = (m - min_cmy)
    y = (y - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale

def cal_rgb(path):
    # 将PDF文件转换为图像列表
    pages = convert_from_path(path, dpi=30)
    BGR = [0, 0, 0]

    # 遍历图像列表并提取CMYK值
    page = pages[0]
    cv_image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
    for i in range(len(cv_image)):
        for j in range(len(cv_image[i])):
            BGR[0] += (cv_image[i][j][0]/(len(cv_image)*len(cv_image[0])*len(pages)))
            BGR[1] += (cv_image[i][j][1]/(len(cv_image)*len(cv_image[0])*len(pages)))
            BGR[2] += (cv_image[i][j][2]/(len(cv_image)*len(cv_image[0])*len(pages)))
    # 提取图像中的CMYK值
    BGR[0]=BGR[0]
    BGR[1]=BGR[1]
    BGR[2]=BGR[2]

    # cmyk=rgb_to_cmyk(BGR[2],BGR[1],BGR[0])
    return [BGR[2],BGR[1],BGR[0]]


def get_dominant_color(path):
    pages = convert_from_path(path, dpi=30)
    image = pages[0]
    max_score = 0.0001
    dominant_color = None
    for count, (r, g, b) in image.getcolors(image.size[0] * image.size[1]):
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13,235)
        y = (y - 16.0) / (235 - 16)
        if y > 0.9:
            continue
        score = (saturation+0.1)*count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    a = [dominant_color[0],dominant_color[1],dominant_color[2]]
    return a

