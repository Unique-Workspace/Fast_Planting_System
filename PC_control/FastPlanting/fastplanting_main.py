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

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

from xbee import ZigBee
import serial
import sys,string
import time

BROADCAST_ADDR_LONG = b'\x00\x00\x00\x00\x00\x00\xff\xff'
BROADCAST_ADDR_SHORT = b'\xff\xfe'

class SerialDialogFrame(QtGui.QDialog, Ui_SerialDialog):
    def __init__(self, serial_port=None, baund_rate=None):
        super(SerialDialogFrame, self).__init__()

        self.serialport = serial_port
        self.baundrate = baund_rate
        self.setupUi(self)
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

        QtCore.QObject.connect(self.button_scan, QtCore.SIGNAL(_fromUtf8("clicked()")), self.scan_node)
        QtCore.QObject.connect(self.button_open_serial, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open_serial)
        QtCore.QObject.connect(self.menu_config_serial, QtCore.SIGNAL(_fromUtf8("triggered()")), self.config_serial)

        self.item_model = QtGui.QStandardItemModel(0, 2, self)
        self.item_model.setHeaderData(0, QtCore.Qt.Horizontal, u"物理地址")
        self.item_model.setHeaderData(1, QtCore.Qt.Horizontal, u"网络地址")

        self.listTableView.setModel(self.item_model)

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

    def update_listview(self, data):
        # put the (addr_long, addr_short) to dictionary.
        self.addr_dict[data[0]] = data[1]

        # 如果找到item，更新到这一行; 如果没有，增加新行;如果有多行，全部删除，重新建一行(不应出现多行的情况)。
        for item in self.ui_mainwindow.item_model.findItems(data[0]):
            self.ui_mainwindow.item_model.setData(self.ui_mainwindow.item_model.index(item.row(), 0, QtCore.QModelIndex()), data[0])
            self.ui_mainwindow.item_model.setData(self.ui_mainwindow.item_model.index(item.row(), 1, QtCore.QModelIndex()), data[1])
            break
        else:
            #print 'else'
            self.ui_mainwindow.item_model.insertRows(self.listrow, 1, QtCore.QModelIndex())
            self.ui_mainwindow.item_model.setData(self.ui_mainwindow.item_model.index(self.listrow, 0, QtCore.QModelIndex()), data[0])
            self.ui_mainwindow.item_model.setData(self.ui_mainwindow.item_model.index(self.listrow, 1, QtCore.QModelIndex()), data[1])

    def message_received(self, data):
        try:
            orig_str = data['rf_data']  # dict assign to string
            src_addr_long = data['source_addr_long']
            src_addr_short = data['source_addr']
            self.update_listview((src_addr_long.encode('hex'), src_addr_short.encode('hex')))
        except Exception, e:    # Except for receive empty Rx data while sending Tx data.
            print e
            return
        try:
            '''数据结构：字符串类型 '湿度，温度，水温' '''
            #print orig_str
            text = orig_str.split(',')
            humidity = text[0]
            temperature_room = text[1]
            temperature_water = text[2]
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            text = 'H:' + humidity + ' Tr:' + temperature_room + ' Tw:' + temperature_water + ' ' + now_time
            print text
        except Exception, e:
            print e
            pass

    def run(self):
        while not self.abort:
            #print 'xbee thread run.'
            try:
                if self.serial.isOpen() and self.serial.inWaiting():
                    # print 'serial is ok'
                    data = self.xbee.wait_read_frame()
                    self.message_received(data)

                time.sleep(1)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = FastPlantingFrame()
    w.show()
    sys.exit(app.exec_())