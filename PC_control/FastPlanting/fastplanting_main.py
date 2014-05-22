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
from Ui_MainWindow import Ui_MainWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

from xbee import ZigBee
import serial
import sys,string
import time
import threading


class FastPlantingFrame(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(FastPlantingFrame, self).__init__()

        self.setupUi(self)

        QtCore.QObject.connect(self.scanButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.scan_node)

        self.xbee_thread = XbeeThread()
        self.xbee_thread.xbee_thread_start()

        print 'FastPlantingFrame init.'

    def __del__(self):

        self.xbee_thread.xbee_thread_stop()
        self.xbee_thread.wait()   # must call wait() to quit the xbee thread.
        print 'FastPlantingFrame del.'

    def scan_node(self):
        print 'scan_node.'
        return


class XbeeThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(XbeeThread, self).__init__(parent)

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
        while True:
            time.sleep(2)
            print 'xbee thread run.'
            if self.abort:
                return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = FastPlantingFrame()
    w.show()
    sys.exit(app.exec_())