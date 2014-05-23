#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
fastplanting_main.py

By Kun Ling, 2014
timonkun@gmail.com

This is main program for Fast Planting System.

下一步要做的：1、增加thread class
2、广播扫描包，并接收反馈，显示在list中。

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

        # define serial port
        self.serial = serial.Serial()
        self.serial_port = '/dev/ttyAMA0'
        self.serial_baundrate = 115200
        # Create API object, which spawns a new thread
        self.xbee = ZigBee(self.serial)

        self.xbee_thread = XbeeThread(self.serial, self.xbee)
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
    def __init__(self,  myserial, myxbee):
        super(XbeeThread, self).__init__()

        self.serial = myserial
        self.xbee = myxbee
        self.abort = False
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

    def run(self):
        while not self.abort:
            print 'xbee thread run.'
            try:
                if self.serial.isOpen() and self.serial.inWaiting():
                    # print 'serial is ok'
                    data = self.xbee.wait_read_frame()
                    #self.message_received(data)

                time.sleep(1)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = FastPlantingFrame()
    w.show()
    sys.exit(app.exec_())