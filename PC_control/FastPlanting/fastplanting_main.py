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
#R1_ADDR_LONG = b'\x00\x13\xA2\x00\x40\xB4\x10\x3b'
#R1_ADDR_SHORT = b'\xff\xfe'


class SpinBoxDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        spinbox = QtGui.QDoubleSpinBox(parent)
        if index.column() == 2 or index.column() == 3:
            spinbox.setRange(10.0, 50.0)
        elif index.column() == 4 or index.column() == 5:
            spinbox.setRange(50.0, 100.0)
        elif index.column() == 6 or index.column() == 7:
            spinbox.setRange(10.0, 40.0)
        return spinbox

    def setEditorData(self, spinbox, index):
        value = index.model().data(index, QtCore.Qt.EditRole).toDouble()[0]
        print value
        spinbox.setValue(value)

    def setModelData(self, spinbox, model, index):
        spinbox.interpretText()
        value = spinbox.value()

        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, spinbox, option, index):
        spinbox.setGeometry(option.rect)


class ComboxDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        print 'creatEditor'
        if index.column() == 8:
            combo_box = QtGui.QComboBox(parent)
            combo_box.addItem("OFF")
            combo_box.addItem("ON")
            return combo_box
        else:
            return 0  # QtGui.QStyledItemDelegate.createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        combo_box = editor
        if not combo_box:
            return

        print 'setEditorData'
        pos = combo_box.findText(index.model().data(index).toString(), QtCore.Qt.MatchExactly)
        combo_box.setCurrentIndex(pos)

    def setModelData(self, editor, model, index):
        combo_box = editor
        if not combo_box:
            return
        print 'setModelData'
        model.setData(index, combo_box.currentText())

    #def emitCommitData(self):
    #   self.commitData.emit(self.sender())


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

        QtCore.QObject.connect(self.button_open_serial, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open_serial)
        QtCore.QObject.connect(self.menu_config_serial, QtCore.SIGNAL(_fromUtf8("triggered()")), self.config_serial)
        QtCore.QObject.connect(self.pushButton_config, QtCore.SIGNAL(_fromUtf8("clicked()")), self.send_config)

        #self.listTableView.setModel(self.item_model)
        self.table_node_info.horizontalHeader().setDefaultSectionSize(90)
        self.table_node_info.setColumnCount(6)
        self.table_node_info.setHorizontalHeaderLabels((u"物理地址", u"网络地址", u"室温", u"湿度", u"水温", u"LED"))
        self.table_node_info.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        for i in range(1, 6):
            self.table_node_info.horizontalHeader().setResizeMode(i, QtGui.QHeaderView.Stretch)

        for index in range(2, 8):
            self.table_range_display.setItemDelegateForColumn(index, SpinBoxDelegate(self))
        self.table_range_display.setItemDelegateForColumn(8, ComboxDelegate(self))
        self.table_range_display.horizontalHeader().setDefaultSectionSize(90)
        self.table_range_display.setColumnCount(9)
        self.table_range_display.setHorizontalHeaderLabels((u"选中物理地址", u"网络地址", u"最低室温", u"最高室温", u"最低湿度",
                                                            u"最大湿度", u"最低水温", u"最高水温", u"LED"))
        self.table_range_display.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        for i in range(1, 9):
            self.table_range_display.horizontalHeader().setResizeMode(i, QtGui.QHeaderView.Stretch)

        #self.listTableView.setColumnWidth()
        # define serial port
        self.serial = serial.Serial()
        self.serial_port = 'COM26'    # '/dev/ttyAMA0'
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

    def send_config(self):
        # item_checkbox.setCheckState(QtCore.Qt.Checked)
        for row in range(0, self.table_range_display.rowCount()):
            item = self.table_range_display.item(row, 0)
            # enum CheckState {Unchecked-0, PartiallyChecked-1, Checked-2}
            if QtCore.Qt.Checked == item.checkState():
                addr_long_short = []
                addr_long_short.append((self.table_range_display.item(row, 0).text(),
                                 self.table_range_display.item(row, 1).text()))
                temp_min = float(self.table_range_display.item(row, 2).text())
                temp_max = float(self.table_range_display.item(row, 3).text())
                humi_min = float(self.table_range_display.item(row, 4).text())
                humi_max = float(self.table_range_display.item(row, 5).text())
                wtemp_min = float(self.table_range_display.item(row, 6).text())
                wtemp_max = float(self.table_range_display.item(row, 7).text())
                led_ctrl = self.table_range_display.item(row, 8).text()
                print addr_long_short, temp_min, temp_max, humi_min, humi_max, wtemp_min, wtemp_max, led_ctrl

                if led_ctrl == 'OFF':
                    led_status = '0'
                elif led_ctrl == 'ON':
                    led_status = '1'
                else:
                    print '[Error] Unknown LED ctrl.'
                    return

                if temp_min < 0 or temp_min > 50:
                    print '[Error]TempMin out of range: ' + str(temp_min)
                    return
                if temp_max < 0 or temp_max > 50:
                    print '[Error]TempMax out of range: ' + str(temp_max)
                    return
                if temp_max < temp_min:
                    print '[Error]TempMax < TempMin'
                    return

                temp_min_data = str(temp_min)
                temp_max_data = str(temp_max)

                if humi_min < 0 or humi_min > 100:
                    print '[Error]HumMin out of range: ' + str(humi_min)
                    return
                if humi_max < 0 or humi_max > 100:
                    print '[Error]HumMax out of range: ' + str(humi_max)
                    return
                if humi_max < humi_min:
                    print '[Error]HumMax < HumMin'
                    return
                humi_min_data = str(humi_min)
                humi_max_data = str(humi_max)

                if wtemp_min < 0 or wtemp_min > 50:
                    print '[Error]TempWaterMin out of range: ' + str(wtemp_min)
                    return
                if wtemp_max < 0 or wtemp_max > 50:
                    print '[Error]TempWaterMax out of range: ' + str(wtemp_max)
                    return
                if wtemp_max < wtemp_min:
                    print '[Error]TempWaterMax < TempWaterMin'
                    return
                wtemp_min_data = str(wtemp_min)
                wtemp_max_data = str(wtemp_max)

                #格式："TRmin,TRmax,Hmin,Hmax,TWmin,TWmax"
                #      20.0,30.0,90.0,100.0,20.0,35.0
                send_data = temp_min_data + ',' + temp_max_data + ',' + humi_min_data + ',' + humi_max_data + ',' + \
                    wtemp_min_data + ',' + wtemp_max_data + ',' + led_status
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
                        if self.serial.isOpen() and self.serial.inWaiting():
                            response = self.xbee.wait_read_frame()
                            print response
                            self.table_range_display.line_config_status.setText(u'设置成功！')
                except Exception, e:
                        print '[Error]set_config() Transfer Fail!!', e


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
        led_status = '%d' % int(text[3])

        item_addr_long = QtGui.QTableWidgetItem(addr_long)
        item_addr_long.setFlags(item_addr_long.flags() & ~QtCore.Qt.ItemIsEditable)
        item_addr_long.setTextAlignment(QtCore.Qt.AlignCenter)
        item_addr_short = QtGui.QTableWidgetItem(addr_short)
        item_addr_short.setFlags(item_addr_short.flags() & ~QtCore.Qt.ItemIsEditable)
        item_addr_short.setTextAlignment(QtCore.Qt.AlignCenter)
        item_temperature_room = QtGui.QTableWidgetItem(temperature_room)
        item_temperature_room.setFlags(item_temperature_room.flags() & ~QtCore.Qt.ItemIsEditable)
        item_temperature_room.setTextAlignment(QtCore.Qt.AlignCenter)
        item_humidity = QtGui.QTableWidgetItem(humidity)
        item_humidity.setFlags(item_humidity.flags() & ~QtCore.Qt.ItemIsEditable)
        item_humidity.setTextAlignment(QtCore.Qt.AlignCenter)
        item_temperature_water = QtGui.QTableWidgetItem(temperature_water)
        item_temperature_water.setFlags(item_temperature_water.flags() & ~QtCore.Qt.ItemIsEditable)
        item_temperature_water.setTextAlignment(QtCore.Qt.AlignCenter)
        item_led = QtGui.QTableWidgetItem(led_status)
        item_led.setFlags(item_led.flags() & ~QtCore.Qt.ItemIsEditable)
        item_led.setTextAlignment(QtCore.Qt.AlignCenter)

        # 如果找到item，更新到这一行; 如果没有，增加新行;如果有多行，全部删除，重新建一行(不应出现多行的情况,未实现)。
        for item in self.ui_mainwindow.table_node_info.findItems(addr_long, QtCore.Qt.MatchFixedString):
            #print item, item.row(), item.column()
            #item.setText(data[0])
            self.ui_mainwindow.table_node_info.setItem(item.row(), 1, item_addr_short)
            self.ui_mainwindow.table_node_info.setItem(item.row(), 2, item_temperature_room)
            self.ui_mainwindow.table_node_info.setItem(item.row(), 3, item_humidity)
            self.ui_mainwindow.table_node_info.setItem(item.row(), 4, item_temperature_water)
            self.ui_mainwindow.table_node_info.setItem(item.row(), 5, item_led)
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
            self.ui_mainwindow.table_node_info.setItem(row, 5, item_led)

        # Create range display config Tab view.
        item_range_addr_long = QtGui.QTableWidgetItem(addr_long)
        item_range_addr_long.setData(QtCore.Qt.UserRole, addr_long)
        item_range_addr_long.setFlags(item_range_addr_long.flags() & ~QtCore.Qt.ItemIsEditable)
        item_range_addr_long.setTextAlignment(QtCore.Qt.AlignCenter)
        item_range_addr_long.setCheckState(QtCore.Qt.Checked)
        item_range_addr_short = QtGui.QTableWidgetItem(addr_short)
        item_range_addr_short.setData(QtCore.Qt.UserRole, addr_short)
        item_range_addr_short.setFlags(item_range_addr_short.flags() & ~QtCore.Qt.ItemIsEditable)
        item_range_addr_short.setTextAlignment(QtCore.Qt.AlignCenter)

        item_range_tmin = QtGui.QTableWidgetItem('20.0')
        item_range_tmin.setTextAlignment(QtCore.Qt.AlignCenter)
        item_range_tmax = QtGui.QTableWidgetItem('30.0')
        item_range_tmax.setTextAlignment(QtCore.Qt.AlignCenter)
        item_range_hmin = QtGui.QTableWidgetItem('90.0')
        item_range_hmin.setTextAlignment(QtCore.Qt.AlignCenter)
        item_range_hmax = QtGui.QTableWidgetItem('100.0')
        item_range_hmax.setTextAlignment(QtCore.Qt.AlignCenter)
        item_range_wtmin = QtGui.QTableWidgetItem('20.0')
        item_range_wtmin.setTextAlignment(QtCore.Qt.AlignCenter)
        item_range_wtmax = QtGui.QTableWidgetItem('35.0')
        item_range_wtmax.setTextAlignment(QtCore.Qt.AlignCenter)

        if led_status == '0':
            item_range_led = QtGui.QTableWidgetItem('OFF')
        else:
            item_range_led = QtGui.QTableWidgetItem('ON')
        item_range_led.setTextAlignment(QtCore.Qt.AlignCenter)
        for item in self.ui_mainwindow.table_range_display.findItems(addr_long, QtCore.Qt.MatchFixedString):
            #self.ui_mainwindow.table_range_display.setItem(item.row(), 0, item_range_addr_long)
            pass
            break
        else:
            row = self.ui_mainwindow.table_range_display.rowCount()
            self.ui_mainwindow.table_range_display.setRowCount(row + 1)
            self.ui_mainwindow.table_range_display.setItem(row, 0, item_range_addr_long)
            self.ui_mainwindow.table_range_display.setItem(row, 1, item_range_addr_short)
            self.ui_mainwindow.table_range_display.setItem(row, 2, item_range_tmin)
            self.ui_mainwindow.table_range_display.setItem(row, 3, item_range_tmax)
            self.ui_mainwindow.table_range_display.setItem(row, 4, item_range_hmin)
            self.ui_mainwindow.table_range_display.setItem(row, 5, item_range_hmax)
            self.ui_mainwindow.table_range_display.setItem(row, 6, item_range_wtmin)
            self.ui_mainwindow.table_range_display.setItem(row, 7, item_range_wtmax)
            self.ui_mainwindow.table_range_display.setItem(row, 8, item_range_led)

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
                    #print data
                    self.message_received(data, database)

                time.sleep(1)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = FastPlantingFrame()
    w.show()
    sys.exit(app.exec_())
