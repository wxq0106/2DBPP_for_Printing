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
        self.setWindowTitle("拼版程序")
        self.resize(int(screen_width * 2 / 3), int(screen_height * 2 / 3))
        conLayout = QVBoxLayout()  # 整体上下布局
        higherlayout = QHBoxLayout()  # 上层是左右布局
        rightgrid = QGridLayout()  # 最上层网格布局
        leftgrid1 = QGridLayout()  # 最上层网格布局
        leftgrid2 = QGridLayout()
        leftgrid3 = QGridLayout()
        midlayout = QHBoxLayout()  # 中间也是左右布局

        # 高层


        self.checkboxs = []
        self.checkboxs1 = []
        self.checkboxs2 = []
        self.checkboxs3 = []
        frame = QFrame()  # 创建实例
        frame.setFrameStyle(QFrame.Box)  # 框架样式
        frame1 = QFrame()  # 创建实例
        frame1.setFrameStyle(QFrame.Box)  # 框架样式
        frame2 = QFrame()  # 创建实例
        frame2.setFrameStyle(QFrame.Box)  # 框架样式
        self.printer = pd.read_sql(f"SELECT uuid,machineName,modelId FROM `t_base_machine`",conn)
        # printer_num = self.json_data["printer"]["printer_num"]
        for i in range(1):
            self.checkbox = QCheckBox()
            # self.checkbox.setText(self.json_data["printer"]["printer_name"][i])
            self.checkbox.setText(self.printer["machineName"][i])
            # if self.json_data["printer"]["printer_state"][i]:
            #     self.checkbox.setChecked(True)
            self.checkbox.setChecked(True)
            leftgrid1.addWidget(self.checkbox, int(i / 4), i % 4)
            self.checkboxs.append(self.checkbox)

        self.setcheckbox("10模", 1, 0, leftgrid1, self.checkboxs1)
        self.setcheckbox("8模", 1, 1, leftgrid1, self.checkboxs1)
        self.setcheckbox("5模", 1, 2, leftgrid1, self.checkboxs1)
        self.setcheckbox("132模", 2, 0, leftgrid1, self.checkboxs1)
        self.setcheckbox("96模", 2, 1, leftgrid1, self.checkboxs1)
        self.setcheckbox("46模", 2, 2, leftgrid1, self.checkboxs1)
        # higherlayout.addLayout(leftgrid1)
        frame.setLayout(leftgrid1)
        higherlayout.addWidget(frame)

        for i in range(4, 5):
            self.checkbox = QCheckBox()
            # self.checkbox.setText(self.json_data["printer"]["printer_name"][i])
            self.checkbox.setText(self.printer["machineName"][i])
            # if self.json_data["printer"]["printer_state"][i]:
            #     self.checkbox.setChecked(True)
            self.checkbox.setChecked(True)
            leftgrid2.addWidget(self.checkbox, 0, (i - 1) % 3)
            self.checkboxs.append(self.checkbox)

        self.setcheckbox("16模", 1, 0, leftgrid2, self.checkboxs2)
        self.setcheckbox("10模", 1, 1, leftgrid2, self.checkboxs2)
        self.setcheckbox("8模", 2, 0, leftgrid2, self.checkboxs2)
        # higherlayout.addLayout(leftgrid2)
        frame1.setLayout(leftgrid2)
        higherlayout.addWidget(frame1)

        self.checkbox = QCheckBox()
        # self.checkbox.setText(self.json_data["printer"]["printer_name"][i])
        self.checkbox.setText(self.printer["machineName"][5])
        # if self.json_data["printer"]["printer_state"][i]:
        #     self.checkbox.setChecked(True)
        self.checkbox.setChecked(True)
        leftgrid3.addWidget(self.checkbox, 0, 0)
        self.checkboxs.append(self.checkbox)
        self.setcheckbox("96模", 1, 0, leftgrid3, self.checkboxs3)
        self.setcheckbox("46模", 1, 1, leftgrid3, self.checkboxs3)
        self.setcheckbox("8模(590)", 2, 0, leftgrid3, self.checkboxs3)
        self.setcheckbox("8模(596)", 2, 1, leftgrid3, self.checkboxs3)
        # higherlayout.addLayout(leftgrid3)
        frame2.setLayout(leftgrid3)
        higherlayout.addWidget(frame2)

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
        self.character_tabel.setHorizontalHeaderLabels(['选择订单类型', '纸张克重', '打印数量','总模数'])
        self.character_tabel.setFixedWidth(600)

        self.choice_all =QPushButton("选择所有类别")
        self.choice_none =QPushButton("清除所有选择")
        self.choice_none.clicked.connect(self.fchoice_none)
        self.choice_all.clicked.connect(self.fchoice_all)
        self.choice_all.setFixedSize(150, 40)
        self.choice_none.setFixedSize(150, 40)

        self.choicebut = QPushButton("查看待拼版订单表")
        self.choicebut.clicked.connect(self.getorder)
        self.choicebut.setFixedSize(150, 40)

        self.characterbut = QPushButton("查看拼版订单类型")
        self.characterbut.clicked.connect(self.getcharacter)
        self.characterbut.setFixedSize(150, 40)

        midleftlayout.addWidget(self.character_tabel)
        midleftdownlayout.addWidget(self.choice_all,0 ,0)
        midleftdownlayout.addWidget(self.choice_none,1 ,0)
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
        self.tableWidget1.setHorizontalHeaderLabels(['订单ID', '交货时间', '下单时间', '纸张克重', '打印数量'])
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
        self.iterlabel = QLabel("遗传优化算法迭代次数")
        self.iterlabel.setAlignment(Qt.AlignCenter)
        self.iteration = QLineEdit(str(self.json_data["default"]["iteration"]))
        # self.iteration.setFixedHeight(40)
        midrightlayout.addWidget(self.iterlabel)
        midrightlayout.addWidget(self.iteration)
        # self.iteration.setFixedWidth(200)

        self.inputlabel = QLabel("最大选择订单数")
        self.inputlabel.setAlignment(Qt.AlignCenter)
        self.inputmaxnum = QLineEdit(str(self.json_data["default"]["max_order"]))
        midrightlayout.addWidget(self.inputlabel)
        midrightlayout.addWidget(self.inputmaxnum)
        self.inputmaxnum.setDisabled(True)

        self.starttime = f'SELECT MIN(scheduleTime) FROM `t_plate_orderchecked` WHERE plated = 0'
        self.endtime = f'SELECT max(scheduleTime) FROM `t_plate_orderchecked` WHERE plated = 0'

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

        self.timelabel = QLabel("未拼版订单时间总跨度")
        self.timelabel.setAlignment(Qt.AlignCenter)
        self.timelabel.setFixedHeight(20)
        self.timebrowser = QTextBrowser()
        # self.timebrowser.setGeometry(QRect(50, 180, 500, 300))
        timegap = a + "    到    " + c
        self.timebrowser.setText(timegap)

        midrightlayout.addWidget(self.timelabel)
        midrightlayout.addWidget(self.timebrowser)

        self.start = QLabel("拼版订单交货开始时间")
        self.start.setAlignment(Qt.AlignCenter)
        self.end = QLabel("拼版订单交货结束时间")
        self.end.setAlignment(Qt.AlignCenter)
        self.choicetime1 = QDateTimeEdit()
        startdat = QDate(self.startyear, self.startmouth, self.startday)
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

        self.makeupbut = QPushButton("开始自动拼版计算")
        self.makeupbut.setFixedSize(150, 40)
        self.makeupbut.clicked.connect(self.makeuprun)

        self.stop = QPushButton("停止自动拼版计算")
        self.stop.setFixedSize(150, 40)
        self.stop.clicked.connect(self.stoprun)

        self.loadbut = QPushButton("写入已拼版文件")
        self.loadbut.clicked.connect(self.load)
        self.loadbut.setFixedSize(150, 40)

        midrightdownlayout.addWidget(self.makeupbut,0,0)
        midrightdownlayout.addWidget(self.stop, 1, 0)
        midrightdownlayout.addWidget(self.loadbut, 0, 1)

        midrightlayout.addLayout(midrightdownlayout)
        midlayout.addLayout(midrightlayout)
        conLayout.addLayout(midlayout)

        # 下层展示
        self.resulttext = QTextEdit()
        # self.timebrowser.setGeometry(QRect(50, 180, 500, 300))
        self.resulttext.setText("运行结果")
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
            f"SELECT distinct specsPaper , specsAmount , productName FROM `t_plate_orderchecked` WHERE specsPaper!='' AND plated = 0 and (productName ='合版名片' or productName ='合版单页') and (scheduleTime between {starttime} and {endtime}) order by specsPaper,specsAmount desc",
            conn)
        self.character_tabel.setRowCount(self.character_inf.shape[0])
        for i in range(self.character_inf.shape[0]):
            total_moshu = 0
            specspaper = '"'+self.character_inf.loc[i][0]+'"'
            amount = self.character_inf.loc[i][1]
            moshu = pd.read_sql(
                f"SELECT totalMoShu FROM `t_plate_orderchecked` WHERE specsPaper={specspaper} and specsAmount={amount} and (productName ='合版名片' or productName ='合版单页') AND plated = 0 and (scheduleTime between {starttime} and {endtime}) order by specsPaper,specsAmount desc",
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
                    total_moshu=QTableWidgetItem(str(total_moshu))
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
        specs = self.find_all_choice_class()
        starttime = self.choicetime1.text()
        endtime = self.choicetime2.text()
        starttime = starttime.replace(".", "-")
        starttime = '"' + starttime + '"'
        endtime = endtime.replace(".", "-")
        endtime = '"' + endtime + '"'
        for i in range(len(specs)):
            if i == 0:
                self.orderinf = pd.read_sql(
                f"SELECT uuid , scheduleTime, orderTime, specsPaper, specsAmount FROM `t_plate_orderchecked` WHERE specsPaper =  {specs[i][1]} and specsAmount = {specs[i][0]} and  plated = 0  AND scheduleTime between {starttime} and {endtime} order by scheduleTime,orderTime",
                conn)
            else:
                orderinf = pd.read_sql(
                    f"SELECT uuid , scheduleTime, orderTime, specsPaper, specsAmount FROM `t_plate_orderchecked` WHERE specsPaper =  {specs[i][1]} and specsAmount = {specs[i][0]} and  plated = 0  AND scheduleTime between {starttime} and {endtime} order by scheduleTime,orderTime",
                    conn)
                self.orderinf = pd.concat([self.orderinf, orderinf], axis=0).reset_index(drop=True)
        self.tableWidget1.clear()
        self.tableWidget1.setHorizontalHeaderLabels(['订单ID', '交货时间', '下单时间', '纸张克重', '打印数量'])
        row = self.orderinf.shape[0]
        self.tableWidget1.setRowCount(row)
        for i in range(row):
            for j in range(self.orderinf.shape[1]):
                oneinf = self.orderinf.loc[i][j]
                # oneinf = one[j]
                if j == 1 or j ==2:
                    oneinf = pd.Timestamp(oneinf).strftime('%Y-%m-%d %H:%M:%S')
                if j == 4:
                    oneinf = str(oneinf)
                newItem = QTableWidgetItem(oneinf)
                self.tableWidget1.setItem(i, j, newItem)
        self.orderinf.drop(self.orderinf.index, inplace=True)

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
                           self.plate["jobNoPrefix"][i],
                           False)
            self.plates.append(epalte)

        ps_plate = pd.read_sql("SELECT uuid,storeAmount,psName FROM `t_base_ps`", conn)
        machine_model = pd.read_sql("SELECT uuid,psId FROM `t_base_machinemodel` WHERE psId != ''",conn)

        check = 0
        for i in [0, 4, 6]:
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
                            ps_name = ps_plate["psName"][k]
                            break

            all_plates = self.plates
            plates = []
            if self.printer["modelId"][i] == "c59b006a7ab843b0a5c87579d9537107":
                duplex_print_type = 1 #单面打印
            else:
                duplex_print_type = 0 #双面打印
            for j in range(len(all_plates)):
                if self.printer["modelId"][i] == all_plates[j].machineid:
                    plates.append(all_plates[j])
                    size = [self.plate["boardWidth"][j], self.plate["boardHeight"][j]]

            eprinter = printer(self.printer["machineName"][i],
                               self.checkboxs[check].isChecked(),
                               0,  # self.json_data["printer"]["work_time"][i],
                               plates,
                               size,
                               duplex_print_type,
                               self.printer["modelId"][i],
                               remain,
                               ps_name)

            check += 1
            self.printers.append(eprinter)
        self.set_plates_state()
        character = self.find_all_choice_class()
        with open('./load.json', 'r', encoding='utf8') as fp2:
            used_item = json.load(fp2)
        self.used_item = used_item["used_item"]
        self.mp = makeup(self, conn, starttime, endtime,  readpath, writepath, num, self.printers, self.plates,character,self.used_item)
        self.mp.sinOut.connect(self.outputbrowser)
        self.mp.start()

    def find_all_choice_class(self):
        character = []
        if self.character_inf is None:
            print("选择")
            return
        for i in range(len(self.character_inf)):
            if self.character_tabel.item(i,0).checkState():
                specspaper =  '"'+self.character_tabel.item(i,1).text()+'"'
                amount = '"'+self.character_tabel.item(i,2).text()+'"'
                if self.character_inf["productName"][i] == '合版名片' and (self.character_inf["specsPaper"][i] == '单Y' or self.character_inf["specsPaper"][i] == '单T'):
                    character.append(['"' + str(self.character_inf["specsAmount"][i]) + '"', '"' + str(self.character_inf["specsPaper"][i]) + '"', False, 1])
                    continue
                elif self.character_inf["productName"][i] == '合版名片':
                    character.append(['"' + str(self.character_inf["specsAmount"][i]) + '"', '"' + str(self.character_inf["specsPaper"][i]) + '"', True, 1])
                elif self.character_inf["productName"][i] == '合版单页':
                    character.append(['"' + str(self.character_inf["specsAmount"][i]) + '"', '"' + str(self.character_inf["specsPaper"][i]) + '"', True, 0])
        return character

    def set_plates_state(self):#根据大版选择的checkbox可以打印的大版
        if self.checkboxs[0].isChecked():
            if self.checkboxs1[0].isChecked():
                self.set_plate_state('c30b359825004dba8a112debcd95d423')
                self.set_plate_state('47cfb7c9f7c645148eb2cf79b5f422c3')
                self.set_print_type('47cfb7c9f7c645148eb2cf79b5f422c3')
            if self.checkboxs1[1].isChecked() :
                self.set_plate_state('927a676398554565aa96b4be9d44e974')
                self.set_plate_state('f9fdc38896cd40ad96d8b4270fb80ea7')
                self.set_print_type('f9fdc38896cd40ad96d8b4270fb80ea7')
            if self.checkboxs1[2].isChecked() :
                self.set_plate_state('4a6988589c6d40d08510d95acbd491f0')
                # self.set_plate_state('f9fdc38896cd40ad96d8b4270fb80ea7')
                # self.set_print_type('f9fdc38896cd40ad96d8b4270fb80ea7')
            if self.checkboxs1[3].isChecked() :
                self.set_plate_state('1f0cdd36903e481586dccf1199a83f07')
                # self.set_plate_state('ceb0d46334ab41aa824e8b7db09bdeb8')
                # self.set_print_type('0789d4d990da4bc69fc8f82929c3b296')
            if self.checkboxs1[4].isChecked() :
                self.set_plate_state('ce358457af2d45f7b2ae26c78209e133')
                self.set_plate_state('ceb0d46334ab41aa824e8b7db09bdeb8')
                self.set_print_type('ceb0d46334ab41aa824e8b7db09bdeb8')
            # if self.checkboxs1[5].isChecked() :
                # self.set_plate_state('ce358457af2d45f7b2ae26c78209e133')

        if self.checkboxs[1].isChecked():
            if self.checkboxs2[0].isChecked():
                self.set_plate_state('3cab4fd8a894460ab9af3dc1452c2b08')
                self.set_plate_state('0789d4d990da4bc69fc8f82929c3b296')
                self.set_print_type('0789d4d990da4bc69fc8f82929c3b296')
            if self.checkboxs2[1].isChecked() :
                self.set_plate_state('6c97f86f5f9d41ff92e7320d0f9b025c')
            if self.checkboxs2[2].isChecked() :
                self.set_plate_state('de5009794f8d47a088320f01ec9e2be1')

        if self.checkboxs[2].isChecked():
            if self.checkboxs3[0].isChecked():
                self.set_plate_state('4a232ad60c6841d18e8256fb5e5b5df1')
                self.set_plate_state('11ef4954ede246d69e247adc25f2ab6d')
                self.set_print_type('11ef4954ede246d69e247adc25f2ab6d')
            if self.checkboxs3[1].isChecked() :
                self.set_plate_state('ffcc3f27557c4d9494d10e1bbdb903f1')
            if self.checkboxs3[2].isChecked() :
                self.set_plate_state('392fc75610fd4bb18f060275eef25eba')
                self.set_plate_state('6d9721c5639c4efb9f6dd4e4c4eeaa77')
                self.set_print_type('6d9721c5639c4efb9f6dd4e4c4eeaa77')
            if self.checkboxs3[3].isChecked() :
                self.set_plate_state('774048d32b5a484d90e5934513ea5ce5')
                self.set_plate_state('4dcebca726b64af5bcd3594f6e8be729')
                self.set_print_type('4dcebca726b64af5bcd3594f6e8be729')

    def load(self):

        for i in range(len(self.used_item)):
            used_item["used_item"].append(self.used_item[i])
        jso = json.dumps(used_item)
        with open('load.json', "w") as js:
            js.write(jso)

    def outputbrowser(self, str):
        self.resulttext.setText(self.resulttext.toPlainText() + str + '\n')
        self.resulttext.moveCursor(QTextCursor.End)

    def closeEvent(self, a0: QCloseEvent):
        for i in range(len(self.printer)):
            check = self.checkboxs[i].isChecked()
            self.json_data["printer"]["printer_state"][i] = check
        self.json_data["default"]["iteration"] = self.iteration.text()

        self.json_data["default"]["max_order"] = self.inputmaxnum.text()
        jso = json.dumps(self.json_data, indent=1)
        with open('jsondata.json', "w",newline='\n') as js:
            js.write(jso)

    def setcheckbox(self,name, i, j, grid,checkboxs):
        self.checkbox = QCheckBox()
        # self.checkbox.setText(self.json_data["printer"]["printer_name"][i])
        self.checkbox.setText(name)
        # if self.json_data["printer"]["printer_state"][i]:
        #     self.checkbox.setChecked(True)
        self.checkbox.setChecked(True)
        grid.addWidget(self.checkbox, i, j)
        checkboxs.append(self.checkbox)

    def set_plate_state(self,num): #设置大版可否打印
        a = list(filter(lambda x: x.num == num, self.plates))
        a[0].state = True

    def set_print_type(self,num):#设置单面打印还是双面打印
        a = list(filter(lambda x: x.num == num, self.plates))
        a[0].duplex_print_type = 1


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
