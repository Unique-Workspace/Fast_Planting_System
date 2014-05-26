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
import sys,string
import time

BROADCAST_ADDR_LONG = b'\x00\x00\x00\x00\x00\x00\xff\xff'
BROADCAST_ADDR_SHORT = b'\xff\xfe'
R1_ADDR_LONG = b'\x00\x13\xA2\x00\x40\xB4\x10\x3b'
R1_ADDR_SHORT = b'\xff\xfe'

class ConfigDialogFrame(QtGui.QDialog, Ui_ConfigDialog):
    def __init__(self, Serial, Xbee):
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
        print 'ConfigDialogFrame init.'

    def __del__(self):
        print 'ConfigDialogFrame del.'

    def close_config(self):
        self.reject()

    def set_config(self):
        print self.spinBox_tmin.value()
        print self.spinBox_tmax.value()
        print self.spinBox_hmin.value()
        print self.spinBox_hmax.value()
        print self.spinBox_wtmin.value()
        print self.spinBox_wtmax.value()
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

        tempra_min_data = 'TRmin:' + str(tempra_min)
        tempra_max_data = 'TRmax:' + str(tempra_max)
        print tempra_min_data
        try:
            # Send Tx packet Temperature min
            if self.serial.isOpen():
                self.xbee.send('tx', frame_id='A', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(tempra_min_data))

            # Wait for response
            #if self.Serial.isOpen() and self.Serial.inWaiting():
            #    response = self.Xbee.wait_read_frame()
            #    print response

            # Send Tx packet Temperature max
            if self.serial.isOpen():
                self.xbee.send('tx', frame_id='B', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(tempra_max_data))

            # Wait for response
            #if self.Serial.isOpen() and self.Serial.inWaiting():
            #    response = self.Xbee.wait_read_frame()
            #    print response
        except Exception, e:
                print '[Error]set_config() Transfer Fail!!', e

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
        humi_min_data = 'Hmin:' + str(humi_min)
        humi_max_data = 'Hmax:' + str(humi_max)
        try:
            # Send Tx packet Humidity min
            if self.serial.isOpen():
                self.xbee.send('tx', frame_id='C', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(humi_min_data))

            # Wait for response
            #if self.Serial.isOpen() and self.Serial.inWaiting():
            #    response = self.Xbee.wait_read_frame()
            #    print response

            # Send Tx packet Humidity max
            if self.serial.isOpen():
                self.xbee.send('tx', frame_id='D', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(humi_max_data))

            # Wait for response
            #if self.Serial.isOpen() and self.Serial.inWaiting():
            #    response = self.Xbee.wait_read_frame()
            #    print response
        except Exception, e:
            print '[Error]set_config() Transfer Fail!!', e

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
        temp_water_min_data = 'TWmin:' + str(temp_water_min)
        temp_water_max_data = 'TWmax:' + str(temp_water_max)
        try:
            # Send Tx packet Humidity min
            if self.serial.isOpen():
                self.xbee.send('tx', frame_id='E', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(temp_water_min_data))

            # Wait for response
            #if self.Serial.isOpen() and self.Serial.inWaiting():
            #    response = self.Xbee.wait_read_frame()
            #    print response

            # Send Tx packet Humidity max
            if self.serial.isOpen():
                self.xbee.send('tx', frame_id='F', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(temp_water_max_data))

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

        QtCore.QObject.connect(self.button_scan, QtCore.SIGNAL(_fromUtf8("clicked()")), self.scan_node)
        QtCore.QObject.connect(self.button_open_serial, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open_serial)
        QtCore.QObject.connect(self.menu_config_serial, QtCore.SIGNAL(_fromUtf8("triggered()")), self.config_serial)
        QtCore.QObject.connect(self.pushButton_setting, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open_configdialog)

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

    def open_configdialog(self):
        config_dialog = ConfigDialogFrame(self.serial, self.xbee)
        ret = config_dialog.exec_()
        print 'open_configdialog done.'


class XbeeThread(QtCore.QThread):
    tempChanged = QtCore.pyqtSignal(str)
    humiChanged = QtCore.pyqtSignal(str)
    watertempChanged = QtCore.pyqtSignal(str)
    ledChanged = QtCore.pyqtSignal(str)

    def __init__(self,  myserial, myxbee, mainwindow):
        super(XbeeThread, self).__init__()

        self.serial = myserial
        self.xbee = myxbee
        self.ui_mainwindow = mainwindow
        self.abort = False
        self.listrow = 0

        self.tempChanged.connect(self.ui_mainwindow.tempLcd.display)
        self.humiChanged.connect(self.ui_mainwindow.humiLcd.display)
        self.watertempChanged.connect(self.ui_mainwindow.watertempLcd.display)
        self.ledChanged.connect(self.ui_mainwindow.ledLcd.display)

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

    def update_clientdata(self, data):
        humidity = '%4.2f' % float(data[0])
        temperature_room = '%4.2f' % float(data[1])
        temperature_water = '%4.2f' % float(data[2])
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        text = 'H:' + humidity + ' Tr:' + temperature_room + ' Tw:' + temperature_water + ' ' + now_time
        print text

        self.tempChanged.emit(temperature_room)
        self.humiChanged.emit(humidity)
        self.watertempChanged.emit(temperature_water)


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
            src_addr_long = data['source_addr_long']
            src_addr_short = data['source_addr']
            self.update_listview((src_addr_long.encode('hex'), src_addr_short.encode('hex')))
        except Exception, e:    # Except for receive empty Rx data while sending Tx data.
            print e
            return
        try:
            '''数据结构：字符串类型 '湿度，温度，水温' '''
            orig_str = data['rf_data']  # dict assign to string
            text = orig_str.split(',')
            self.update_clientdata(text)
        except Exception, e:
            print e
            return

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