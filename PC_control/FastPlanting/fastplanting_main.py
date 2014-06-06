#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
fastplanting_main.py

By Kun Ling, 2014
timonkun@gmail.com

This is main program for Fast Planting System.

下一步要做的：1、在窗体右侧显示节点数据信息
2、广播扫描包，并接收反馈，显示在list中。
3、窗体右侧显示多点数据信息

"""
__author__ = 'lingkun'

from PyQt4 import QtCore, QtGui
from UI_MainWindow import Ui_MainWindow
from UI_SerialDialog import Ui_SerialDialog
from UI_ConfigDialog import Ui_ConfigDialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

from xbee import ZigBee
import serial
import sys, string
import time
from database import RecordDb

BROADCAST_ADDR_LONG = b'\x00\x00\x00\x00\x00\x00\xff\xff'
BROADCAST_ADDR_SHORT = b'\xff\xfe'
R1_ADDR_LONG = b'\x00\x13\xA2\x00\x40\xB4\x10\x3b'
R1_ADDR_SHORT = b'\xff\xfe'

class ImageDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        comboBox = QtGui.QComboBox(parent)
        if index.column() == 7:
            comboBox.addItem(u"关闭")
            comboBox.addItem(u"打开")

        #comboBox.activated.connect(self.emitCommitData)

        return comboBox

    def setEditorData(self, editor, index):
        comboBox = editor
        if not comboBox:
            return

        pos = comboBox.findText(index.model().data(index),
                QtCore.Qt.MatchExactly)
        comboBox.setCurrentIndex(pos)

    def setModelData(self, editor, model, index):
        comboBox = editor
        if not comboBox:
            return

        model.setData(index, comboBox.currentText())

    #def emitCommitData(self):
    #   self.commitData.emit(self.sender())

class ConfigDialogFrame(QtGui.QDialog, Ui_ConfigDialog):
    def __init__(self, Serial, Xbee, mainwindow):
        super(ConfigDialogFrame, self).__init__()

        self.setupUi(self)

        self.spinBox_tmax.setValue(30.0)
        self.spinBox_tmin.setValue(20.0)
        self.spinBox_tmax.setRange(10.0, 50.0)
        self.spinBox_tmin.setRange(10.0, 50.0)

        self.spinBox_hmax.setValue(100.0)
        self.spinBox_hmin.setValue(90.0)
        self.spinBox_hmax.setRange(50.0, 100.0)
        self.spinBox_hmin.setRange(50.0, 100.0)

        self.spinBox_wtmax.setValue(35.0)
        self.spinBox_wtmin.setValue(20.0)
        self.spinBox_wtmax.setRange(10.0, 50.0)
        self.spinBox_wtmin.setRange(10.0, 50.0)

        QtCore.QObject.connect(self.pushButton_config, QtCore.SIGNAL(_fromUtf8("clicked()")), self.set_config)
        QtCore.QObject.connect(self.pushButton_close, QtCore.SIGNAL(_fromUtf8("clicked()")), self.close_config)

        self.serial = Serial
        self.xbee = Xbee
        self.ui_mainwindow = mainwindow

        print 'ConfigDialogFrame init.'

    def __del__(self):
        print 'ConfigDialogFrame del.'

    def close_config(self):
        self.reject()

    def set_config(self):

        addr_long_short = []
        # item_checkbox.setCheckState(QtCore.Qt.Checked)
        for row in range(0, self.ui_mainwindow.table_node_info.rowCount()):
            item = self.ui_mainwindow.table_node_info.item(row, 6)
            # enum CheckState {Unchecked-0, PartiallyChecked-1, Checked-2}
            if QtCore.Qt.Checked == item.checkState():
                addr_long_short.append((self.ui_mainwindow.table_node_info.item(row, 0).text(),
                                 self.ui_mainwindow.table_node_info.item(row, 1).text()))

        tempra_min = self.spinBox_tmin.value()
        tempra_max = self.spinBox_tmax.value()
        if tempra_min < 0 or tempra_min > 50:
            print '[Error]TempMin out of range: ' + tempra_min
            return
        if tempra_max < 0 or tempra_max > 50:
            print '[Error]TempMax out of range: ' + tempra_max
            return
        if tempra_max < tempra_min:
            print '[Error]TempMax < TempMin'
            return

        tempra_min_data = str(tempra_min)
        tempra_max_data = str(tempra_max)

        humi_min = self.spinBox_hmin.value()
        humi_max = self.spinBox_hmax.value()
        if humi_min < 0 or humi_min > 100:
            print '[Error]HumMin out of range: ' + humi_min
            return
        if humi_max < 0 or humi_max > 100:
            print '[Error]HumMax out of range: ' + humi_max
            return
        if humi_max < humi_min:
            print '[Error]HumMax < HumMin'
            return
        humi_min_data = str(humi_min)
        humi_max_data = str(humi_max)

        temp_water_min = self.spinBox_wtmin.value()
        temp_water_max = self.spinBox_wtmax.value()
        if temp_water_min < 0 or temp_water_min > 50:
            print '[Error]TempWaterMin out of range: ' + temp_water_min
            return
        if temp_water_max < 0 or temp_water_max > 50:
            print '[Error]TempWaterMax out of range: ' + temp_water_max
            return
        if temp_water_max < temp_water_min:
            print '[Error]TempWaterMax < TempWaterMin'
            return
        temp_water_min_data = str(temp_water_min)
        temp_water_max_data = str(temp_water_max)

        #格式："TRmin,TRmax,Hmin,Hmax,TWmin,TWmax"
        #      20.0,30.0,90.0,100.0,20.0,35.0
        send_data = tempra_min_data + ',' + tempra_max_data + ',' + humi_min_data + ',' + humi_max_data + ',' + \
            temp_water_min_data + ',' + temp_water_max_data
        print send_data
        try:
            for addr in addr_long_short:
                addr_long = str(addr[0]).decode('hex')
                addr_short = str(addr[1]).decode('hex')
                print addr_long, addr_short

                # Send Tx packet Temperature min
                if self.serial.isOpen():
                    self.xbee.send('tx', frame_id='A', dest_addr_long=addr_long, dest_addr=addr_short,
                               data=str(send_data))

                # Wait for response
                #if self.Serial.isOpen() and self.Serial.inWaiting():
                #    response = self.Xbee.wait_read_frame()
                #    print response
        except Exception, e:
                print '[Error]set_config() Transfer Fail!!', e


class SerialDialogFrame(QtGui.QDialog, Ui_SerialDialog):
    def __init__(self, serial_port=None, baund_rate=None):
        super(SerialDialogFrame, self).__init__()

        self.setupUi(self)

        self.serialport = serial_port
        self.baundrate = baund_rate
        self.comboBox_Serial.setEditText(serial_port)
        self.comboBox_BaundRate.setEditText(str(baund_rate))
        QtCore.QObject.connect(self.pushButton_confirm, QtCore.SIGNAL(_fromUtf8("clicked()")), self.set_serial_config)

        print 'SerialDialogFrame init.'

    def __del__(self):
        print 'SerialDialogFrame del.'

    def set_serial_config(self):
        self.serialport = self.comboBox_Serial.currentText()
        self.baundrate = self.comboBox_BaundRate.currentText()
        self.accept()

    def get_serial_config(self):
        return self.serialport, self.baundrate


class FastPlantingFrame(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(FastPlantingFrame, self).__init__()

        self.setupUi(self)

        QtCore.QObject.connect(self.button_config, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open_configdialog)
        QtCore.QObject.connect(self.button_open_serial, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open_serial)
        QtCore.QObject.connect(self.menu_config_serial, QtCore.SIGNAL(_fromUtf8("triggered()")), self.config_serial)
        #QtCore.QObject.connect(self.pushButton_setting, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open_configdialog)

        #self.listTableView.setModel(self.item_model)
        self.table_node_info.horizontalHeader().setDefaultSectionSize(90)
        self.table_node_info.setColumnCount(7)
        self.table_node_info.setHorizontalHeaderLabels((u"物理地址", u"网络地址", u"室温", u"湿度", u"水温", u"LED", u"选中配置"))
        self.table_node_info.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.table_node_info.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.table_node_info.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
        self.table_node_info.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.Stretch)
        self.table_node_info.horizontalHeader().setResizeMode(4, QtGui.QHeaderView.Stretch)
        self.table_node_info.horizontalHeader().setResizeMode(5, QtGui.QHeaderView.Stretch)
        self.table_node_info.horizontalHeader().setResizeMode(6, QtGui.QHeaderView.ResizeToContents)
        
        self.table_range_display.setItemDelegate(ImageDelegate(self))
        self.table_range_display.horizontalHeader().setDefaultSectionSize(90)
        self.table_range_display.setColumnCount(8)
        self.table_range_display.setHorizontalHeaderLabels((u"地址选中配置", u"最高室温", u"最低室温", u"最大湿度", u"最低湿度",
                                                            u"最高水温", u"最低水温", u"LED"))
        self.table_range_display.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.table_range_display.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.table_range_display.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
        self.table_range_display.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.Stretch)
        self.table_range_display.horizontalHeader().setResizeMode(4, QtGui.QHeaderView.Stretch)
        self.table_range_display.horizontalHeader().setResizeMode(5, QtGui.QHeaderView.Stretch)
        self.table_range_display.horizontalHeader().setResizeMode(6, QtGui.QHeaderView.Stretch)
        self.table_range_display.horizontalHeader().setResizeMode(7, QtGui.QHeaderView.Stretch)

        #self.listTableView.setColumnWidth()
        # define serial port
        self.serial = serial.Serial()
        self.serial_port = '/dev/ttyAMA0'
        self.serial_baundrate = 115200
        # Create API object, which spawns a new thread
        self.xbee = ZigBee(self.serial)

        self.xbee_thread = XbeeThread(self.serial, self.xbee, self)
        self.xbee_thread.xbee_thread_start()

        print 'FastPlantingFrame init.'

    def __del__(self):
        self.xbee.halt()
        self.serial.close()

        self.xbee_thread.xbee_thread_stop()
        self.xbee_thread.wait()   # must call wait() to quit the xbee thread.
        print 'FastPlantingFrame del.'

    def scan_node(self):
        print 'scan_node.'
        if self.serial.isOpen():
            self.xbee.send('tx', frame_id='A', dest_addr_long=BROADCAST_ADDR_LONG, dest_addr=BROADCAST_ADDR_SHORT, data='broadcast')
        return

    def config_serial(self):
        print 'serial config.'
        serial_dialog = SerialDialogFrame(self.serial_port, self.serial_baundrate)
        ret = serial_dialog.exec_()
        if ret == 1:
            self.serial_port, self.serial_baundrate = serial_dialog.get_serial_config()
            print self.serial_port, self.serial_baundrate
        elif ret == 0:
            print 'discard config.'

    def open_serial(self):
        if not self.serial.isOpen():
            try:
                print self.serial_port, self.serial_baundrate
                self.serial.port = str(self.serial_port)
                self.serial.baudrate = str(self.serial_baundrate)
                self.serial.open()
            except Exception, e:
                print '[Error]COMM Open Fail!!', e
            else:
                self.button_open_serial.setText(u"断开")
                if self.serial.isOpen() and self.serial.inWaiting():
                    print 'serial is connected.'
        else:
            self.serial.close()
            while self.serial.isOpen():
                pass
            self.button_open_serial.setText(u"连接")

    def open_configdialog(self):
        config_dialog = ConfigDialogFrame(self.serial, self.xbee, self)
        ret = config_dialog.exec_()
        print 'open_configdialog done.'


class XbeeThread(QtCore.QThread):
    def __init__(self,  myserial, myxbee, mainwindow):
        super(XbeeThread, self).__init__()

        self.serial = myserial
        self.xbee = myxbee
        self.ui_mainwindow = mainwindow
        self.abort = False
        self.listrow = 0
        self.addr_dict = {}
        print 'XbeeThread init.'

    def __del__(self):
        print 'XbeeThread del.'

    def xbee_thread_start(self):
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def xbee_thread_stop(self):
        if self.isRunning():
            self.abort = True
        else:
            print 'stop do nothing.'

    def update_database(self, addr_long, data, database):
        dict_data = {}
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        dict_data['node_id'] = str(addr_long)
        dict_data['node_time'] = now_time
        dict_data['node_humi'] = data[0]
        dict_data['node_temp'] = data[1]
        dict_data['node_watertemp'] = data[2]
        database.do_write(dict_data)

    def update_table_nodeinfo(self, data, text):
        # put the (addr_long, addr_short) to dictionary.
        #self.addr_dict[data[0]] = data[1]
        addr_long = data[0]
        addr_short = data[1]
        humidity = '%4.2f' % float(text[0])
        temperature_room = '%4.2f' % float(text[1])
        temperature_water = '%4.2f' % float(text[2])

        item_checkbox = QtGui.QTableWidgetItem()
        item_checkbox.setFlags(item_checkbox.flags() & ~QtCore.Qt.ItemIsEditable)

        item_addr_long = QtGui.QTableWidgetItem(addr_long)
        item_addr_long.setFlags(item_addr_long.flags() & ~QtCore.Qt.ItemIsEditable)
        item_addr_short = QtGui.QTableWidgetItem(addr_short)
        item_addr_short.setFlags(item_addr_short.flags() & ~QtCore.Qt.ItemIsEditable)
        item_temperature_room = QtGui.QTableWidgetItem(temperature_room)
        item_temperature_room.setFlags(item_temperature_room.flags() & ~QtCore.Qt.ItemIsEditable)
        item_humidity = QtGui.QTableWidgetItem(humidity)
        item_humidity.setFlags(item_humidity.flags() & ~QtCore.Qt.ItemIsEditable)
        item_temperature_water = QtGui.QTableWidgetItem(temperature_water)
        item_temperature_water.setFlags(item_temperature_water.flags() & ~QtCore.Qt.ItemIsEditable)
        
        

        # 如果找到item，更新到这一行; 如果没有，增加新行;如果有多行，全部删除，重新建一行(不应出现多行的情况,未实现)。
        for item in self.ui_mainwindow.table_node_info.findItems(addr_long, QtCore.Qt.MatchFixedString):
            #print item, item.row(), item.column()
            #item.setText(data[0])
            self.ui_mainwindow.table_node_info.setItem(item.row(), 1, item_addr_short)
            self.ui_mainwindow.table_node_info.setItem(item.row(), 2, item_temperature_room)
            self.ui_mainwindow.table_node_info.setItem(item.row(), 3, item_humidity)
            self.ui_mainwindow.table_node_info.setItem(item.row(), 4, item_temperature_water)
            # do not change item_checkbox

            break
        else:
            #print 'else'
            row = self.ui_mainwindow.table_node_info.rowCount()
            self.ui_mainwindow.table_node_info.setRowCount(row + 1)
            self.ui_mainwindow.table_node_info.setItem(row, 0, item_addr_long)
            self.ui_mainwindow.table_node_info.setItem(row, 1, item_addr_short)
            self.ui_mainwindow.table_node_info.setItem(row, 2, item_temperature_room)
            self.ui_mainwindow.table_node_info.setItem(row, 3, item_humidity)
            self.ui_mainwindow.table_node_info.setItem(row, 4, item_temperature_water)
            item_checkbox.setCheckState(QtCore.Qt.Checked)
            self.ui_mainwindow.table_node_info.setItem(row, 6, item_checkbox)
            
        item_range_addr_long = QtGui.QTableWidgetItem(addr_long)
        item_range_led = QtGui.QTableWidgetItem(u'关闭')
        #item_range_led.setText(u'关闭')
        for item in self.ui_mainwindow.table_range_display.findItems(addr_long, QtCore.Qt.MatchFixedString):
            #self.ui_mainwindow.table_range_display.setItem(item.row(), 0, item_range_addr_long)
            pass
            break
        else:
            row = self.ui_mainwindow.table_range_display.rowCount()
            self.ui_mainwindow.table_range_display.setRowCount(row + 1)
            self.ui_mainwindow.table_range_display.setItem(row, 0, item_range_addr_long)
            self.ui_mainwindow.table_range_display.setItem(row, 7, item_range_led)
            #self.ui_mainwindow.table_range_display.openPersistentEditor(item_range_led)

    def message_received(self, data, database):
        try:
            src_addr_long = data['source_addr_long']
            src_addr_short = data['source_addr']

            '''数据结构：字符串类型 '湿度，温度，水温' '''
            orig_str = data['rf_data']  # dict assign to string
            text = orig_str.split(',')
            self.update_table_nodeinfo((src_addr_long.encode('hex'), src_addr_short.encode('hex')), text)
            self.update_database(src_addr_long.encode('hex'), text, database)
        except Exception, e:
            print e

    def run(self):
        database = RecordDb()
        while not self.abort:
            #print 'xbee thread run.'
            try:
                if self.serial.isOpen() and self.serial.inWaiting():

                    data = self.xbee.wait_read_frame()
                    print data
                    self.message_received(data, database)

                time.sleep(1)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = FastPlantingFrame()
    w.show()
    sys.exit(app.exec_())
