#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
fastplanting_main.py

By Kun Ling, 2014
timonkun@gmail.com

This is main program for Fast Plant Growing System.
"""

from PyQt4 import QtCore, QtGui
from UI_MainWindow import Ui_MainWindow
from UI_SerialDialog import Ui_SerialDialog
from UI_ConfigDialog import Ui_ConfigDialog
from XbeeThread import XbeeThread
from xbee import ZigBee
import serial
import copy
import sys
import os
import commands
from config_process import ConfigProcess
import plot_display

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

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


class TimeDialogFrame(QtGui.QDialog, Ui_ConfigDialog):
    def __init__(self):
        super(TimeDialogFrame, self).__init__()

        self.setupUi(self)

        QtCore.QObject.connect(self.pushButton_confirm, QtCore.SIGNAL(_fromUtf8("clicked()")), self.set_timedate)
        self.time = None
        self.date = None
        print self.timeEdit.displayFormat()
        print self.dateEdit.displayFormat()
        #print 'TimeDialogFrame init.'

    def __del__(self):
        pass
        #print 'TimeDialogFrame del.'

    def set_timedate(self):
        self.time = self.timeEdit.time()
        self.date = self.dateEdit.date()
        self.accept()

    def get_timedate(self):
        if self.time is not None and self.date is not None:
            return self.time, self.date
        else:
            return None


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
        self.showMaximized()

        QtCore.QObject.connect(self.button_open_serial, QtCore.SIGNAL(_fromUtf8("clicked()")), self.open_serial)
        QtCore.QObject.connect(self.button_scan, QtCore.SIGNAL(_fromUtf8("clicked()")), self.scan_node)
        QtCore.QObject.connect(self.menu_scan_node, QtCore.SIGNAL(_fromUtf8("triggered()")), self.scan_node)
        QtCore.QObject.connect(self.menu_config_serial, QtCore.SIGNAL(_fromUtf8("triggered()")), self.config_serial)
        QtCore.QObject.connect(self.pushButton_config, QtCore.SIGNAL(_fromUtf8("clicked()")), self.send_config)
        QtCore.QObject.connect(self.pushButton_save, QtCore.SIGNAL(_fromUtf8("clicked()")), self.save_config)
        QtCore.QObject.connect(self.menu_save_config, QtCore.SIGNAL(_fromUtf8("triggered()")), self.save_config)
        QtCore.QObject.connect(self.table_plot_node, QtCore.SIGNAL(_fromUtf8("itemClicked(QTableWidgetItem*)")), self.refresh_plot)
        QtCore.QObject.connect(self.combo_plot_range, QtCore.SIGNAL(_fromUtf8("activated(int)")), self.redraw_plot_event)
        QtCore.QObject.connect(self.button_setup_time, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setup_time)
        QtCore.QObject.connect(self.menu_update_online, QtCore.SIGNAL(_fromUtf8("triggered()")), self.update_online)

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

        self.table_plot_node.horizontalHeader().setDefaultSectionSize(90)
        self.table_plot_node.setColumnCount(1)
        self.table_plot_node.setHorizontalHeaderLabels((u"物理地址",))
        self.table_plot_node.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)

        self.qwt_plot = plot_display.PlotDisplay(self.qwtPlot, self.combo_plot_range.currentIndex())
        self.selected_plot_node = {}
        self.selected_plot_node['row'] = -1    # default value
        self.selected_plot_node['text'] = ''
        
        self.selected_combo_range = 0

        self.show_clock_time()
        clock_timer = QtCore.QTimer(self)
        clock_timer.timeout.connect(self.show_clock_time)
        clock_timer.start(1000)

        self.plot_timer = QtCore.QTimer(self)
        self.plot_timer.timeout.connect(self.plot_timer_event)

        # define serial port
        self.serial = serial.Serial()
        self.serial_port = '/dev/ttyAMA0'
        self.serial_baundrate = 115200
        # Create API object, which spawns a new thread
        self.xbee = ZigBee(self.serial)

        self.xbee_thread = XbeeThread(self.serial, self.xbee, self)
        self.xbee_thread.xbee_thread_start()
        
        self.open_serial()
        print 'FastPlantingFrame init.'

    def __del__(self):
        print 'FastPlantingFrame del111.'
        self.xbee.halt()
        self.serial.close()

        self.xbee_thread.xbee_thread_stop()
        self.xbee_thread.wait()   # must call wait() to quit the xbee thread.
        print 'FastPlantingFrame del.'

    def update_online(self):
        update_cmd = 'cd /home/pi/Workspace/Fast_Planting_System/Raspi/FastPlanting && git pull'
        #output = os.popen(update_cmd)
        (status, output) = commands.getstatusoutput(update_cmd)
        if status == 0 and output == 'Already up-to-date.':
            self.plainTextEdit.setText(u'已经是最新版本，无需更新。')
        elif status == 0:
            self.plainTextEdit.setText(u'在线更新成功！系统将自动重启，请稍等...')
            (status2, output2) = commands.getstatusoutput('sudo reboot')
            print status2, output2
        else:
            self.plainTextEdit.setText(u'在线更新失败！')
            print status, output


    def setup_time(self):
        time_dialog = TimeDialogFrame()
        ret = time_dialog.exec_()
        if ret == 1:
            current_time, current_date = time_dialog.get_timedate()
            current_time = str(current_time.toString('hh:mm:ss'))
            current_date = str(current_date.toString('yyyyMMdd'))
            time_cmd = 'sudo date -s ' + current_time
            date_cmd = 'sudo date -s ' + current_date
            os.popen(date_cmd)
            os.popen(time_cmd)
        elif ret == 0:
            print 'discard config.'

    def redraw_plot_event(self, selected_index):
        if selected_index == self.selected_combo_range:
            print 'redraw_plot return 0.'
            return 0
        self.selected_combo_range = selected_index
        self.redraw_plot(selected_index)
    
    # 每一次重置显示范围，都要从数据库中读取对应数据，进行解析，不要使用PlotDisplay类中的本地数据。
    def redraw_plot(self, selected_index):
        if self.plot_timer.isActive():
            self.plot_timer.stop()
        time_limit = plot_display.PlotDisplay.get_plot_time_limit(selected_index)
        self.qwt_plot.redraw_plot(time_limit)
        if time_limit != plot_display.ALL_TIME_STATIC:
            self.plot_timer.start(plot_display.MONITOR_DELAY_TIME)

    # 用户点击节点地址条目，触发此函数进行对应条目的数据显示。
    # 应当从数据库中读取数据进行显示。
    def refresh_plot(self, selected_item):
        new_selected_row = selected_item.row()
        if new_selected_row != self.selected_plot_node['row']:
            self.selected_plot_node['row'] = new_selected_row
            self.selected_plot_node['text'] = str(selected_item.text())
            self.qwt_plot.selected_plot_node = copy.deepcopy(self.selected_plot_node)  # 保持选中节点同步
            time_limit = plot_display.PlotDisplay.get_plot_time_limit(self.combo_plot_range.currentIndex())
            if time_limit != plot_display.ALL_TIME_STATIC:  # 判断是否为静态显示。
                if self.plot_timer.isActive():
                    self.qwt_plot.clean_plot()
                    self.plot_timer.stop()
                self.redraw_plot(self.combo_plot_range.currentIndex())
                #self.plot_timer.start(plot_display.MONITOR_DELAY_TIME)    # 延时不需太短，5~10s为宜, 注意此timer在多次启动后能否自动回收, 待测试。
                print 'start plot timer.'
            else:
                self.qwt_plot.redraw_plot(time_limit)   # 进行静态显示。
                print 'ALL_TIME_STATIC.'
        else:
            print 'already selected ' + str(new_selected_row)

    # For the QwtPlot display
    def plot_timer_event(self):
        # 此处应该载入从数据库读出的历史数据，以列表形式传递给 self.qwt_plot.update_plot 进行刷新。
        # 然后再往下执行，加上当前数据更新。
        if 'text' in self.selected_plot_node.keys() and self.selected_plot_node['text'] == ''and \
            'row' in self.selected_plot_node.keys() and self.selected_plot_node['row'] == -1:
            return 
        if self.table_node_info.rowCount() > 0:
            sensor_data = {}
            if 'row' in self.selected_plot_node.keys() and self.selected_plot_node['row'] != -1:
                item = self.table_node_info.item(self.selected_plot_node['row'], 0)
                if 'text' in self.selected_plot_node.keys() and item.text() != self.selected_plot_node['text']:   # 选中节点不存在，则清除plot,并返回.
                    print 'plot_timer_event - clean ' + self.selected_plot_node['text']
                    self.qwt_plot.clean_plot()
                    self.selected_plot_node['row'] = -1
                    self.selected_plot_node['text'] = ''
                    self.qwt_plot.selected_plot_node = copy.deepcopy(self.selected_plot_node)    # 保持选中节点同步
                    self.plot_timer.stop()
                    return
            print self.selected_plot_node
            item = self.table_node_info.item(self.selected_plot_node['row'], 2)  # 室内温度
            temp_room = float(item.text())
            item = self.table_node_info.item(self.selected_plot_node['row'], 3)  # 湿度
            humidity = float(item.text())
            item = self.table_node_info.item(self.selected_plot_node['row'], 4)  # 水温
            temp_water = float(item.text())
            if self.qwt_plot.base_msec == 0:
                self.qwt_plot.base_msec = QtCore.QDateTime.currentMSecsSinceEpoch()
            sensor_data[plot_display.TROOM] = float(temp_room)
            sensor_data[plot_display.HUMIDITY] = float(humidity)
            sensor_data[plot_display.TWATER] = float(temp_water)
            self.qwt_plot.update_plot(sensor_data)

        elif self.table_node_info.rowCount() <= 0:  # 列表空，则清除plot
            print 'plot_timer_event - clean ' + self.selected_plot_node['text']
            self.qwt_plot.clean_plot()
            self.selected_plot_node['row'] = -1
            self.selected_plot_node['text'] = ''
            self.qwt_plot.selected_plot_node = self.selected_plot_node  # 保持选中节点同步
            self.plot_timer.stop()
    # For the QwtPlot display

    def show_clock_time(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm:ss')
        self.lcdNumber_time.display(text)

        date = QtCore.QDate.currentDate()
        text = date.toString('yyyy.MM.dd')
        self.lcdNumber_date.display(text)

    def scan_node(self):
        print 'scan_node.'
        if self.serial.isOpen():
            self.xbee.send('tx', frame_id='S', dest_addr_long=BROADCAST_ADDR_LONG, dest_addr=BROADCAST_ADDR_SHORT, data='scan')
        else:
            self.plainTextEdit.setText(u'未连接串口！')

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
                self.scan_node()
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

                led_status = '1' if led_ctrl == 'ON' else '0'

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
                #print send_data
                self.send_config_func(addr_long_short, send_data)

    def send_config_func(self, addr_long_short, send_data):
        try:
            for addr in addr_long_short:
                addr_long = str(addr[0]).decode('hex')
                addr_short = str(addr[1]).decode('hex')
                
                #print addr_long_short, send_data
                #print addr_long, addr_short

                # Send Tx packet Temperature min
                if self.serial.isOpen():
                    self.xbee.send('tx', frame_id='A', dest_addr_long=addr_long, dest_addr=addr_short,
                                data=str(send_data))

                # Wait for response
                if self.serial.isOpen() and self.serial.inWaiting():
                    response = self.xbee.wait_read_frame()
                    #print response
                    self.line_config_status.setText(u'设置成功！')
        except Exception, e:
                print '[Error]set_config() Transfer Fail!!', e

    def save_config(self):
        config = ConfigProcess()
        config.load_config()
        for row in range(0, self.table_range_display.rowCount()):
            # enum CheckState {Unchecked-0, PartiallyChecked-1, Checked-2}
            addr_long = str(self.table_range_display.item(row, 0).text())
            temp_min = self.table_range_display.item(row, 2).text()
            temp_max = self.table_range_display.item(row, 3).text()
            humi_min = self.table_range_display.item(row, 4).text()
            humi_max = self.table_range_display.item(row, 5).text()
            wtemp_min = self.table_range_display.item(row, 6).text()
            wtemp_max = self.table_range_display.item(row, 7).text()
            led_ctrl = self.table_range_display.item(row, 8).text()
            
            led = '1' if led_ctrl == 'ON' else '0'
            config_data = (addr_long, temp_min, temp_max, humi_min, humi_max, wtemp_min, wtemp_max, led)
            config.set_config_value(config_data)

        config.save_config()
        self.line_config_status.setText(u'配置保存成功！')


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = FastPlantingFrame()
    w.show()
    sys.exit(app.exec_())
