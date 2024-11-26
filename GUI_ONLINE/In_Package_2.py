# WXQ
# 时间： $(DATE) $(TIME)
from item_2 import item
from package_2 import package

from item_2 import re_rotate


# from geneticsAlgoritham_1 import GeneticsAlgoritham


def put_in_package(Items, Package, num, package_order, new_package):
    # if Item.size_x >Package[num-1].size_x or Item.size_y > Package[num-1].size_y :
    #     print("尺寸超标")
    all_in = False
    for i in range(len(Items)):
        Items[i].index = -1

    while len(Items) != 0 and Package[num].in_package == True:  # 直到小箱子排完，或没有箱子能排进当前大箱子里
        if Package[num].wight == 0:
            Package[num].put_in_y(Items)
        else:
            Package[num].put_in_4(Items)

    if new_package:
        while len(Items) != 0:
            if Package[num].wight == 0:
                Package[num].put_in_y(Items)
            else:
                Package[num].put_in_4(Items)

            while Package[num].in_package == False:
                if (num + 1) >= len(package_order):
                    return True
                b = Package[num].new_package(package_order[num + 1][0], package_order[num + 1][1])
                b.put_in_y(Items)
                Package.append(b)
                num += 1
    return all_in


def set_gene(gene, items):  # 将基因对应的信息赋值给每个小箱子
    a = []
    for i in range(len(items)):
        a.append(items[gene[i]])
    return a


# def draw_bins(squares,number_of_bins,bin_size_x,bin_size_y):
#     step=10
#     im_dim_x=(max(bin_size_x)+2)*step
#     im_dim_y = 0
#     for i in range(number_of_bins):
#         im_dim_y += (bin_size_y[i]+1)*step
#     im = Image.new('RGB', (im_dim_x, im_dim_y), (256, 256, 256))
#     draw = ImageDraw.Draw(im)
#
#     number_of_drawn_bins=0
#     bin_pos_y = step
#     #while(number_of_drawn_bins<number_of_bins):#判断是否到达最后一个箱子
#     for i in range(number_of_bins):
#         bin_pos_x=step
#         if i!=0:
#             bin_pos_y += (((bin_size_y[i-1]+1)*step))
#         draw.rectangle((bin_pos_x, bin_pos_y, bin_pos_x+bin_size_x[i]*step, bin_pos_y+bin_size_y[i]*step), fill=(51, 102, 255), outline=(0, 0, 26))
#         squares_for_bin=list(filter(lambda x: x.index== i, squares))#删除不在这个箱子中的盒子
#         if(len(squares_for_bin)>0):
#             draw_squares(squares_for_bin,step,draw,bin_pos_x,bin_pos_y)#画出处于这个箱子中的盒子
#             number_of_drawn_bins+=1 #箱子序号加一
#
#
#     im.save('bins.jpg', quality=95)
#
# def draw_squares(squares_for_bin,step,draw,bin_pos_x,bin_pos_y):
#     for square in squares_for_bin:
#         lc_x=bin_pos_x+square.position_x*step
#         lc_y=bin_pos_y+square.position_y*step
#         rc_y=lc_y+square.size_y*step
#         rc_x=lc_x+square.size_x*step
#         draw.rectangle((lc_x, lc_y, rc_x, rc_y), fill=(153, 255, 102), outline=(0, 26, 9))


def in_package(items, gene, cut_in_y, package_order, printed):
    new_order_of_items = set_gene(gene, items)
    # re_rotate(items)
    item_inorder = []
    packages = []
    # for i in range(max(gene)+1):#
    #     a = list(filter(lambda x:x.index == i,items))
    #     item_inorder.append(a)
    #     d = package(package_order[i][0], package_order[i][1])
    #     d.index=i
    #     packages.append(d)
    d = package(package_order[0][0], package_order[0][1])
    d.index = 0
    packages.append(d)

    order = max(gene)

    if cut_in_y:
        # for i in range(len(item_inorder)):
        #     put_in_package(item_inorder[i], packages, i, package_order, False)
        #     for j in range(len(item_inorder[i])):
        #         remains.append(item_inorder[i][j])
        #
        # while len(remains) != 0:
        #     num =len(packages)-1
        #     a = put_in_package(remains,packages,num,package_order,True)
        #     if a:
        #         break

        all_in = put_in_package(new_order_of_items, packages, 0, package_order, True)


    # else:
    #     packages[0].rot_package()
    #     for i in range(len(item_inorder)):
    #         items[i].rot_item()
    #         num = len(packages)
    #         for j in range(len(package_order)):
    #             package_order[j][0],package_order[j][1]=package_order[j][1],package_order[j][0]
    #         put_in_package(item_inorder[i], packages, num,order,package_order)
    #         for j in range(len(item_inorder[i])):
    #             remains.append(item_inorder[i][j])
    item_area = 0
    b = 0
    remains_area = 0
    # for i in range(len(remains)):
    #     remains_area += remains[i].square

    for i in range(len(items)):
        if b < items[i].index:
            b = items[i].index
    if b == 0:
        area = packages[0].size_x * packages[0].size_y
        for i in range(len(items)):
            item_area += items[i].square
    else:
        for i in range(b):
            a = list(filter(lambda x: x.index == i, items))
            for j in range(len(a)):
                item_area += a[j].square

        item_area -= remains_area

        area = 0
        # for i in range(len(items)):
        #     item_area += items[i].square
        for i in range(b):
            area += packages[i].size_x * packages[i].size_y

    num_of_package = len(packages)

    return -num_of_package + item_area / area, items, packages

# num = len(packages)
# put_in_package(b[1],packages,num)
# num = len(packages)
# put_in_package(b[2],packages,num)
# num = len(packages)
# put_in_package(b[3],packages,num)
# num = len(packages)
# put_in_package(b[4],packages,num)
# num = len(packages)
# put_in_package(b[5],packages,num)
# num = len(packages)
# put_in_package(b[6],packages,num)
# num = len(packages)
# put_in_package(b[7],packages,num)
# num = len(packages)
# put_in_package(b[8],packages,num)
# num = len(packages)
# put_in_package(b[9],packages,num)
# num = len(packages)
# put_in_package(b[10],packages,num)
