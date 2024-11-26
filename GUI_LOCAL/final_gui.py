# WXQ
# 时间： $(DATE) $(TIME)
import pymysql
import pandas as pd
from PyQt5.QtWidgets import *
import sys

from PyQt5.Qt import *
from PyQt5.QtWidgets import *
import pymysql
import numpy as np
from main_2 import makeup
import pandas as pd
import win32api
import json
from printer import printer
from plate import plate
import math



# from log_data import QComboBoxDemo
# '230406123449'
class show_result(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(QWidget, self).__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        self.json_data = json_data
        self.mp = 0
        self.character_inf = None
        self.used_item = used_item["used_item"]
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        self.setWindowTitle("Automatic Imposition System")
        self.resize(int(screen_width * 2 / 3), int(screen_height * 2 / 3))
        conLayout = QVBoxLayout()  # 整体上下布局
        higherlayout = QHBoxLayout()  # 上层是左右布局
        rightgrid = QGridLayout()  # 最上层网格布局
        leftgrid = QGridLayout()  # 最上层网格布局
        midlayout = QHBoxLayout()  # 中间也是左右布局

        # 高层

        self.checkboxs = []
        self.printer = pd.read_sql(f"SELECT uuid,machineName,modelId FROM `t_base_machine`", conn)
        # printer_num = self.json_data["printer"]["printer_num"]
        for i in range(len(self.printer)):
            self.checkbox = QCheckBox()
            # self.checkbox.setText(self.json_data["printer"]["printer_name"][i])
            self.checkbox.setText(self.printer["machineName"][i])
            # if self.json_data["printer"]["printer_state"][i]:
            #     self.checkbox.setChecked(True)
            self.checkbox.setChecked(True)
            leftgrid.addWidget(self.checkbox, int(i / 4), i % 4)
            self.checkboxs.append(self.checkbox)
        higherlayout.addLayout(leftgrid)
        HL = QWidget()
        HL.setLayout(higherlayout)
        HL.setFixedHeight(200)
        conLayout.addWidget(HL)

        # 中层

        # self.orderinf = pd.read_sql(
        #     "SELECT uuid , scheduleTime, orderTime, specsPaper, amount FROM `t_plate_order` WHERE "
        #     "specsPaper!='' order by scheduleTime,orderTime", conn)
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        midleftlayout = QVBoxLayout()
        midleftdownlayout = QGridLayout()
        self.character_tabel = QTableWidget()
        # self.character_tabel.setRowCount(self.character_inf.shape[0])
        self.character_tabel.setColumnCount(4)
        self.character_tabel.setColumnWidth(0, 130)
        self.character_tabel.setColumnWidth(1, 180)
        self.character_tabel.setColumnWidth(2, 100)
        self.character_tabel.setColumnWidth(3, 100)
        self.character_tabel.setHorizontalHeaderLabels(['Order Type', 'Paper Weight', 'Print Number', 'Total Impressions']) #'选择订单类型', '纸张克重', '打印数量', '总模数'
        self.character_tabel.setFixedWidth(600)

        self.choice_all = QPushButton("Select All Categories") #选择所有类别
        self.choice_none = QPushButton("Clear All Selections") #清除所有选择
        self.choice_none.clicked.connect(self.fchoice_none)
        self.choice_all.clicked.connect(self.fchoice_all)
        self.choice_all.setFixedSize(250, 40)
        self.choice_none.setFixedSize(250, 40)

        self.choicebut = QPushButton("Pending Imposition Orders") # 查看待拼版订单表
        self.choicebut.clicked.connect(self.getorder)
        self.choicebut.setFixedSize(250, 40)

        self.characterbut = QPushButton("Imposition Order Types")  # 查看拼版订单类型
        self.characterbut.clicked.connect(self.getcharacter)
        self.characterbut.setFixedSize(250, 40)

        midleftlayout.addWidget(self.character_tabel)
        midleftdownlayout.addWidget(self.choice_all, 0, 0)
        midleftdownlayout.addWidget(self.choice_none, 1, 0)
        midleftdownlayout.addWidget(self.characterbut, 0, 1)
        midleftdownlayout.addWidget(self.choicebut, 1, 1)
        midleftlayout.addLayout(midleftdownlayout)

        # for i in range(self.character_inf.shape[0]):
        #     for j in range(3):
        #
        #         if j == 0:
        #             self.check = QTableWidgetItem()
        #             self.check.setCheckState(Qt.Checked)  # 把checkBox设为未选中状态
        #             self.character_tabel.setItem(i, 0, self.check)
        #             continue
        #         one = self.character_inf.loc[i]
        #         oneinf = str(one[j - 1])
        #         newItem = QTableWidgetItem(oneinf)
        #         self.character_tabel.setItem(i, j, newItem)
        self.tableWidget1 = QTableWidget()
        # self.tableWidget1.setRowCount(self.orderinf.shape[0])
        self.tableWidget1.setColumnCount(5)
        self.tableWidget1.setColumnWidth(0, 400)
        self.tableWidget1.setColumnWidth(1, 200)
        self.tableWidget1.setColumnWidth(2, 300)
        self.tableWidget1.setColumnWidth(3, 100)
        self.tableWidget1.setColumnWidth(4, 100)
        self.tableWidget1.setHorizontalHeaderLabels(['Order ID', 'Delivery Time', 'Order Time', 'Paper Weight', 'Print Number']) #'订单ID', '交货时间', '下单时间', '纸张克重', '打印数量'
        # for i in range(self.orderinf.shape[0]):
        #     for j in range(self.orderinf.shape[1]):
        #
        #         one = self.orderinf.loc[i]
        #         oneinf = one[j]
        #         if j == 2:
        #             oneinf = pd.Timestamp(oneinf).strftime('%Y-%m-%d %H:%M:%S')
        #         if j == 4:
        #             oneinf =str(oneinf)
        #         newItem = QTableWidgetItem(oneinf)
        #         self.tableWidget1.setItem(i, j, newItem)
        midlayout.addLayout(midleftlayout)
        midlayout.addWidget(self.tableWidget1)

        midrightlayout = QVBoxLayout()
        midrightdownlayout = QGridLayout()
        self.iterlabel = QLabel("Number of Iterations") #遗传优化算法迭代次数
        self.iterlabel.setAlignment(Qt.AlignCenter)
        self.iteration = QLineEdit(str(self.json_data["default"]["iteration"]))
        # self.iteration.setFixedHeight(40)
        midrightlayout.addWidget(self.iterlabel)
        midrightlayout.addWidget(self.iteration)
        # self.iteration.setFixedWidth(200)

        self.inputlabel = QLabel("Max Order Selection") #最大选择订单数
        self.inputlabel.setAlignment(Qt.AlignCenter)
        self.inputmaxnum = QLineEdit(str(self.json_data["default"]["max_order"]))
        midrightlayout.addWidget(self.inputlabel)
        midrightlayout.addWidget(self.inputmaxnum)
        self.inputmaxnum.setDisabled(True)

        self.starttime = f'SELECT MIN(scheduleTime) FROM `t_plate_order` WHERE plated = 0'
        self.endtime = f'SELECT max(scheduleTime) FROM `t_plate_order` WHERE plated = 0'

        start = pd.read_sql(self.starttime, con=conn)
        a = str(start.loc[0][0])
        b = a.split('-')
        self.startyear = int(b[0])
        self.startmouth = int(b[1])
        self.startday = int(b[2])
        end = pd.read_sql(self.endtime, con=conn)
        c = str(end.loc[0][0])
        d = c.split('-')
        self.endyear = int(d[0])
        self.endmouth = int(d[1])
        self.endday = int(d[2])

        self.timelabel = QLabel("Pending Orders Time Span") #未拼版订单时间总跨度
        self.timelabel.setAlignment(Qt.AlignCenter)
        self.timelabel.setFixedHeight(20)
        self.timebrowser = QTextBrowser()
        # self.timebrowser.setGeometry(QRect(50, 180, 500, 300))
        timegap = a + "    to    " + c
        self.timebrowser.setText(timegap)

        midrightlayout.addWidget(self.timelabel)
        midrightlayout.addWidget(self.timebrowser)

        self.start = QLabel("Imposition Order Delivery Start Time") #拼版订单交货结束时间
        self.start.setAlignment(Qt.AlignCenter)
        self.end = QLabel("Imposition Order Delivery End Time") #拼版订单交货结束时间
        self.end.setAlignment(Qt.AlignCenter)
        self.choicetime1 = QDateTimeEdit()
        startdat = QDate(self.startyear, self.startmouth, self.startday)
        self.now_date = QDate.currentDate()
        self.settime = QDate.currentDate().addDays(1)
        if startdat <= self.settime:
            startdat = self.settime

        self.choicetime1.setMinimumDate(QDate(self.startyear, self.startmouth, self.startday))
        self.choicetime1.setDate(startdat)
        self.choicetime1.dateChanged.connect(self.setendtime)
        self.choicetime2 = QDateTimeEdit()
        self.choicetime1.setDisplayFormat("yyyy.MM.dd")
        self.choicetime2.setDisplayFormat("yyyy.MM.dd")
        enddat = startdat.addDays(1)
        self.choicetime2.setDate(enddat)
        self.choicetime2.setMinimumDate(QDate(self.startyear, self.startmouth, self.startday))
        midrightlayout.addWidget(self.start)
        midrightlayout.addWidget(self.choicetime1)
        midrightlayout.addWidget(self.end)
        midrightlayout.addWidget(self.choicetime2)
        frame1 = QFrame()  # 创建实例
        frame1.setFrameStyle(QFrame.Box)
        frame1.setLayout(midrightlayout)
        frame1.setFixedWidth(400)
        midlayout.addWidget(frame1)

        self.makeupbut = QPushButton("START")
        self.makeupbut.setFixedSize(150, 40)
        self.makeupbut.clicked.connect(self.makeuprun)

        self.stop = QPushButton("END")
        self.stop.setFixedSize(150, 40)
        self.stop.clicked.connect(self.stoprun)

        self.loadbut = QPushButton("Save Imposed File") #写入已拼版文件
        # self.loadbut.clicked.connect(self.load)
        self.loadbut.setFixedSize(200, 40)

        midrightdownlayout.addWidget(self.makeupbut, 0, 0)
        midrightdownlayout.addWidget(self.stop, 1, 0)
        midrightdownlayout.addWidget(self.loadbut, 0, 1)

        midrightlayout.addLayout(midrightdownlayout)
        midlayout.addLayout(midrightlayout)
        conLayout.addLayout(midlayout)

        # 下层展示
        self.resulttext = QTextEdit()
        # self.timebrowser.setGeometry(QRect(50, 180, 500, 300))
        self.resulttext.setText("Running result")
        self.resulttext.setFixedHeight(300)
        conLayout.addWidget(self.resulttext)

        # conLayout.addWidget(self.checkbox)

        # tableWidget = QTableWidget()
        # tableWidget.setRowCount(6)
        # tableWidget.setColumnCount(3)
        # conLayout.addWidget(tableWidget)
        # tableWidget.setHorizontalHeaderLabels(['姓名  ', '性别', '体重(kg)'])
        # newItem = QTableWidgetItem("张三")
        # tableWidget.setItem(0, 0, newItem)
        # newItem = QTableWidgetItem('男')
        # tableWidget.setItem(0, 1, newItem)
        # newItem = QTableWidgetItem('160')
        # tableWidget.setItem(0, 2, newItem)
        self.setLayout(conLayout)

    def stoprun(self):
        if self.mp == 0:
            return
        else:
            self.mp.sinOut.emit("拼版结束")
            self.mp.terminate()

    def setendtime(self, qdate):
        self.choicetime2.setMinimumDate(qdate)

    def getcharacter(self):
        self.character_tabel.setRowCount(0)
        starttime = self.choicetime1.text()
        endtime = self.choicetime2.text()
        starttime = starttime.replace(".", "-")
        starttime = '"' + starttime + '"'
        endtime = endtime.replace(".", "-")
        endtime = '"' + endtime + '"'
        self.character_inf = pd.read_sql(
            f"SELECT distinct specsPaper , amount , productName FROM `t_plate_order` WHERE specsPaper!='' and (productName ='合版名片' or productName ='合版单页') and filePath != ''  AND specsPaper !='' and (scheduleTime between {starttime} and {endtime}) order by specsPaper,amount DESC",
            conn)
        self.character_tabel.setRowCount(self.character_inf.shape[0])
        for i in range(self.character_inf.shape[0]):
            total_moshu = 0
            specspaper = '"' + self.character_inf.loc[i][0] + '"'
            amount = self.character_inf.loc[i][1]
            moshu = pd.read_sql(
                f"SELECT moshu FROM `t_plate_order` WHERE specsPaper={specspaper} and amount={amount} and (productName ='合版名片' or productName ='合版单页') and filePath != ''  AND specsPaper !=''and (scheduleTime between {starttime} and {endtime}) order by specsPaper,amount DESC",
                conn)
            for m in range(len(moshu)):
                total_moshu += moshu.loc[m][0]
            for j in range(4):
                if j == 0:
                    self.check = QTableWidgetItem()
                    self.check.setCheckState(Qt.Checked)  # 把checkBox设为选中状态
                    self.character_tabel.setItem(i, 0, self.check)
                    continue
                if j == 3:
                    total_moshu = QTableWidgetItem(str(total_moshu))
                    self.character_tabel.setItem(i, 3, total_moshu)
                    continue
                one = self.character_inf.loc[i]
                oneinf = str(one[j - 1])
                newItem = QTableWidgetItem(oneinf)
                self.character_tabel.setItem(i, j, newItem)

    def fchoice_none(self):

        for i in range(self.character_tabel.rowCount()):
            self.check = QTableWidgetItem()
            self.check.setCheckState(Qt.Unchecked)  # 把checkBox设为选中状态
            self.character_tabel.setItem(i, 0, self.check)

    def fchoice_all(self):

        for i in range(self.character_tabel.rowCount()):
            self.check = QTableWidgetItem()
            self.check.setCheckState(Qt.Checked)  # 把checkBox设为选中状态
            self.character_tabel.setItem(i, 0, self.check)

    def getorder(self):
        self.tableWidget1.setRowCount(0)
        if self.inputmaxnum.text() == '':
            QMessageBox.information(self, "提示", "请选择最大订单数")
            return
        num = int(self.inputmaxnum.text())
        starttime = self.choicetime1.text()
        specs = self.find_all_choice_class()

        endtime = self.choicetime2.text()
        starttime = starttime.replace(".", "-")
        starttime = '"' + starttime + '"'
        endtime = endtime.replace(".", "-")
        endtime = '"' + endtime + '"'
        for i in range(len(specs)):
            if i == 0:
                self.orderinf = pd.read_sql(
                    f"SELECT uuid , scheduleTime, orderTime, specsPaper, amount FROM `t_plate_order` WHERE specsPaper = {specs[i][1]} and amount = {specs[i][0]} and (productName ='合版名片' or productName ='合版单页') AND scheduleTime between {starttime} and {endtime} order by scheduleTime,orderTime",
                    conn)
            else:
                orderinf = pd.read_sql(
                    f"SELECT uuid , scheduleTime, orderTime, specsPaper, amount FROM `t_plate_order` WHERE specsPaper = {specs[i][1]} and amount = {specs[i][0]} and (productName ='合版名片' or productName ='合版单页') AND scheduleTime between {starttime} and {endtime} order by scheduleTime,orderTime",
                    conn)
                self.orderinf = pd.concat([self.orderinf, orderinf], axis=0).reset_index(drop=True)
        self.tableWidget1.clear()
        self.tableWidget1.setHorizontalHeaderLabels(['Order ID', 'Delivery Time', 'Order Time', 'Paper Weight', 'Print Number'])
        # if num <= self.orderinf.shape[0]:
        #     row = num
        # else:
        row = self.orderinf.shape[0]
        self.tableWidget1.setRowCount(row)
        for i in range(row):
            for j in range(self.orderinf.shape[1]):
                one = self.orderinf.loc[i]
                oneinf = one[j]
                if j == 2:
                    oneinf = pd.Timestamp(oneinf).strftime('%Y-%m-%d %H:%M:%S')
                if j == 4:
                    oneinf = str(oneinf)
                newItem = QTableWidgetItem(oneinf)
                self.tableWidget1.setItem(i, j, newItem)

    def makeuprun(self):
        if self.inputmaxnum.text() == '':
            QMessageBox.information(self, "提示", "请选择最大订单数")
            return
        starttime = self.choicetime1.text()
        endtime = self.choicetime2.text()
        starttime = starttime.replace(".", "-")
        starttime = '"' + starttime + '"'
        endtime = endtime.replace(".", "-")
        endtime = '"' + endtime + '"'
        readpath = self.json_data["default"]["readpath"]
        writepath = self.json_data["default"]["writepath"]
        num = int(self.inputmaxnum.text())
        self.printers = []
        self.plates = []
        self.plate = pd.read_sql(
            f"SELECT uuid,modelId,boardHeight,boardWidth,printWidth,printHeight,bloodWidth,scaleBoardWidth,gripWidth,jobNoPrefix,coreName FROM `t_plate_core` WHERE jobNoPrefix = 'MP' or jobNoPrefix = 'CY' OR jobNoPrefix = 'NB' AND modelId !=''",
            conn)

        for i in range(len(self.plate)):
            # epalte = plate(self.json_data["plate"]["id"][i],
            #                self.json_data["plate"]["effective_size"][i],
            #                self.json_data["plate"]["remain"][i],
            #                self.json_data["plate"]["model_type"][i],
            #                self.json_data["plate"]["num_model"][i],
            #                self.json_data["plate"]["Seam"][i],
            #                self.json_data["plate"]["scale"][i])
            if self.plate["jobNoPrefix"][i] == 'MP':
                model_type = 1
                single_width = 92
                single_height = 56
            else:
                model_type = 0
                single_width = 210
                single_height = 285
            if np.isnan(self.plate["scaleBoardWidth"][i]):
                scale = 1
            else:
                scale = int((self.plate["scaleBoardWidth"][i] / self.plate["boardWidth"][i]) * 1000) / 1000
            num_model = int(self.plate["printWidth"][i]*self.plate["printHeight"][i]/ (single_width*single_height))
            epalte = plate(self.plate["uuid"][i],
                           self.plate["coreName"][i],
                           [self.plate["printWidth"][i], self.plate["printHeight"][i]],
                           model_type,
                           num_model,  # self.json_data["plate"]["num_model"][i],
                           self.plate["gripWidth"][i],
                           self.plate["bloodWidth"][i],
                           scale,
                           self.plate["modelId"][i],
                           self.plate["jobNoPrefix"][i])
            self.plates.append(epalte)

        ps_plate = pd.read_sql("SELECT uuid,storeAmount FROM `t_base_ps`", conn)
        machine_model = pd.read_sql("SELECT uuid,psId FROM `t_base_machinemodel` WHERE psId != ''",conn)

        for i in range(len(self.printer)):
            # plates = []
            # for j in range(len(self.json_data["printer"]["plate_type"][i])):
            #     plates.append(self.plates[self.json_data["printer"]["plate_type"][i][j]])
            # eprinter = printer(self.json_data["printer"]["printer_name"][i],
            #                    self.checkboxs[i].isChecked(),
            #                    self.json_data["printer"]["work_time"][i],
            #                    plates,
            #                    self.json_data["printer"]["plate_size"][i],
            #                    self.json_data["printer"]["duplex_print_type"][i])
            # self.printers.append(eprinter)
            for j in range(len(machine_model)): #查找材料的剩余
                if self.printer["modelId"][i] == machine_model["uuid"][j]:
                    ps_id = machine_model["psId"][j]
                    for k in range(len(ps_plate)):
                        if ps_id == ps_plate["uuid"][k]:
                            remain = ps_plate["storeAmount"][k]
                            break

            all_plates = self.plates
            plates = []
            if self.printer["modelId"][i] == "c59b006a7ab843b0a5c87579d9537107":
                duplex_print_type = 1
            else:
                duplex_print_type = 0
            for j in range(len(all_plates)):
                if self.printer["modelId"][i] == all_plates[j].machineid:
                    plates.append(all_plates[j])
                    size = [self.plate["boardWidth"][j], self.plate["boardHeight"][j]]


            eprinter = printer(self.printer["machineName"][i],
                               self.checkboxs[i].isChecked(),
                               0,  # self.json_data["printer"]["work_time"][i],
                               plates,
                               size,
                               duplex_print_type,
                               self.printer["modelId"][i],
                               remain)
            self.printers.append(eprinter)
        with open('./load.json', 'r', encoding='utf8') as fp2:
            used_item = json.load(fp2)
        self.used_item = used_item["used_item"]
        character = self.find_all_choice_class()
        self.mp = makeup(self, conn, starttime, endtime, readpath, writepath, num, self.printers, self.plates,
                         character,self.used_item)
        self.mp.sinOut.connect(self.outputbrowser)
        self.mp.start()

    def find_all_choice_class(self):
        character = []
        if self.character_inf is None:
            print("选择")
            return
        for i in range(len(self.character_inf)):
            if self.character_tabel.item(i, 0).checkState():
                specspaper = '"' + self.character_tabel.item(i, 1).text() + '"'
                amount = '"' + self.character_tabel.item(i, 2).text() + '"'
                if self.character_inf["productName"][i] == '合版名片' and (
                        self.character_inf["specsPaper"][i] == '单Y' or self.character_inf["specsPaper"][i] == '单T'):
                    character.append(['"' + str(self.character_inf["amount"][i]) + '"',
                                      '"' + str(self.character_inf["specsPaper"][i]) + '"', False, 1])
                    continue
                elif self.character_inf["productName"][i] == '合版名片':
                    character.append(['"' + str(self.character_inf["amount"][i]) + '"',
                                      '"' + str(self.character_inf["specsPaper"][i]) + '"', True, 1])
                elif self.character_inf["productName"][i] == '合版单页':
                    character.append(['"' + str(self.character_inf["amount"][i]) + '"',
                                      '"' + str(self.character_inf["specsPaper"][i]) + '"', True, 0])
        return character

    def outputbrowser(self, str):
        self.resulttext.setText(self.resulttext.toPlainText() + str + '\n')
        self.resulttext.moveCursor(QTextCursor.End)

    def closeEvent(self, a0: QCloseEvent):
        for i in range(self.json_data["printer"]["printer_num"]):
            check = self.checkboxs[i].isChecked()
            self.json_data["printer"]["printer_state"][i] = check
        self.json_data["default"]["iteration"] = self.iteration.text()

        self.json_data["default"]["max_order"] = self.inputmaxnum.text()
        jso = json.dumps(self.json_data)
        with open('jsondata.json', "w") as js:
            js.write(jso)


if __name__ == "__main__":
    # conn = pymysql.connect(
    #     user='swu2023',  # 用户名
    #     password='SWu.20230608',  # 密码：这里一定要注意123456是字符串形式
    #     host='192.168.1.66',  # 指定访问的服务器，本地服务器指定“localhost”，远程服务器指定服务器的ip地址
    #     database='jperp',  # 数据库的名字
    #     port=3416,  # 指定端口号，范围在0-65535
    #     charset='utf8mb4',  # 数据库的编码方式
    # )
    with open('./jsondata.json', 'r', encoding='utf8') as fp1:
        json_data = json.load(fp1)
    with open('./load.json', 'r', encoding='utf8') as fp2:
        used_item = json.load(fp2)
    conn = pymysql.connect(
        user=json_data["database"]["user"],  # 用户名
        password=json_data["database"]["password"],  # 密码：这里一定要注意123456是字符串形式
        host=json_data["database"]["host"],  # 指定访问的服务器，本地服务器指定“localhost”，远程服务器指定服务器的ip地址
        database=json_data["database"]["database"],  # 数据库的名字
        port=json_data["database"]["port"],  # 指定端口号，范围在0-65535
        charset=json_data["database"]["charset"],  # 数据库的编码方式
    )
    app = QApplication(sys.argv)
    widget = show_result()
    widget.setWindowState(Qt.WindowMaximized)
    widget.show()

    sys.exit(app.exec_())
