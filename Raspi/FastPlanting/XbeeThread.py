#! /usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import time
from config_process import ConfigProcess
from database import RecordDb
import threading
import copy

MONITOR_TIMER_DELAY = 3000

class XbeeThread(QtCore.QThread):
    def __init__(self,  myserial, myxbee, mainwindow):
        super(XbeeThread, self).__init__()

        self.serial = myserial
        self.xbee = myxbee
        self.ui_mainwindow = mainwindow
        self.abort = False
        self.listrow = 0
        self.addr_dict_current = {}
        self.addr_dict_last = {}
        self.refresh_table_timer = QtCore.QTimer(self)
        self.refresh_table_timer.timeout.connect(self.refresh_table_event)
        self.db_timer = QtCore.QTimer(self)
        self.db_timer.timeout.connect(self.update_database_event)
        self.database  = None
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

    def refresh_table_event(self):
        for key in self.addr_dict_last:
            if self.addr_dict_last[key] == self.addr_dict_current[key]:
                for item in self.ui_mainwindow.table_node_info.findItems(key, QtCore.Qt.MatchFixedString):
                    #print 'need to delete row=' + str(item.row()) + '  ' + key + '=' + str(self.addr_dict_current[key])
                    self.ui_mainwindow.table_node_info.removeRow(item.row())

                for item in self.ui_mainwindow.table_range_display.findItems(key, QtCore.Qt.MatchFixedString):
                    self.ui_mainwindow.table_range_display.removeRow(item.row())

                for item in self.ui_mainwindow.table_plot_node.findItems(key, QtCore.Qt.MatchFixedString):
                    self.ui_mainwindow.table_plot_node.removeRow(item.row())
        self.addr_dict_last = copy.deepcopy(self.addr_dict_current)
        #self.timer = threading.Timer(MONITOR_TIMER_DELAY, self.timer_func_refresh_table)
        #self.timer.start()

    def update_database_event(self):
        if self.database == None:
            self.database = RecordDb()
        current_row = self.ui_mainwindow.table_node_info.rowCount() 
        if current_row > 0:
            dict_data = {}
            for row in xrange(0, current_row):
                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                dict_data['node_time'] = current_time
                item = self.ui_mainwindow.table_node_info.item(row, 0)
                dict_data['node_id'] = str(item.text())
                item = self.ui_mainwindow.table_node_info.item(row, 2)  # 室内温度
                dict_data['node_temp']  = float(item.text())
                item = self.ui_mainwindow.table_node_info.item(row, 3)  # 湿度
                dict_data['node_humi']  = float(item.text())
                item = self.ui_mainwindow.table_node_info.item(row, 4)  # 水温
                dict_data['node_watertemp']  = float(item.text())
                self.database.do_write(dict_data)

    def update_table_nodeinfo(self, data, text):
        #print data, text
        addr_long = data[0]
        addr_short = data[1]
        humidity = '%5.2f' % float(text[0])
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
            self.addr_dict_current[addr_long] += 1
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
            addr_dict = dict(([addr_long, 0],))
            self.addr_dict_current.update(addr_dict)

        # Create range display CONFIG Tab view.
        item_range_addr_long = QtGui.QTableWidgetItem(addr_long)
        item_range_addr_long.setData(QtCore.Qt.UserRole, addr_long)
        item_range_addr_long.setFlags(item_range_addr_long.flags() & ~QtCore.Qt.ItemIsEditable)
        item_range_addr_long.setTextAlignment(QtCore.Qt.AlignCenter)
        item_range_addr_long.setCheckState(QtCore.Qt.Checked)
        item_range_addr_short = QtGui.QTableWidgetItem(addr_short)
        item_range_addr_short.setData(QtCore.Qt.UserRole, addr_short)
        item_range_addr_short.setFlags(item_range_addr_short.flags() & ~QtCore.Qt.ItemIsEditable)
        item_range_addr_short.setTextAlignment(QtCore.Qt.AlignCenter)

        # table_range_display refresh.
        for item in self.ui_mainwindow.table_range_display.findItems(addr_long, QtCore.Qt.MatchFixedString):
            # Item already exists, do not change.
            #self.ui_mainwindow.table_range_display.setItem(item.row(), 0, item_range_addr_long)

            pass
            break
        else:    # Add new item.
            #  只在初次刷新时，加载一次配置文件，显示到界面。
            # 后面的界面更新就不从配置文件读取了。
            # 初次刷新时，要把参数发送到Arduino端，否则二者不同步。
            # 但是，如果Arduino中途重启，配置就不同步了。
            config = ConfigProcess()
            config.load_config()
            config_info = config.get_config_value(addr_long)
            # (tmin, tmax, hmin, hmax, wtmin, wtmax, led)
            if config_info is not None:
                tmin = config_info[0]
                tmax = config_info[1]
                hmin = config_info[2]
                hmax = config_info[3]
                wtmin = config_info[4]
                wtmax = config_info[5]
                led_status = config_info[6]  # note led_status
            else:
                tmin = '20.0'
                tmax = '30.0'
                hmin = '90.0'
                hmax = '100.0'
                wtmin = '20.0'
                wtmax = '35.0'

            item_range_tmin = QtGui.QTableWidgetItem(tmin)
            item_range_tmin.setTextAlignment(QtCore.Qt.AlignCenter)
            item_range_tmax = QtGui.QTableWidgetItem(tmax)
            item_range_tmax.setTextAlignment(QtCore.Qt.AlignCenter)
            item_range_hmin = QtGui.QTableWidgetItem(hmin)
            item_range_hmin.setTextAlignment(QtCore.Qt.AlignCenter)
            item_range_hmax = QtGui.QTableWidgetItem(hmax)
            item_range_hmax.setTextAlignment(QtCore.Qt.AlignCenter)
            item_range_wtmin = QtGui.QTableWidgetItem(wtmin)
            item_range_wtmin.setTextAlignment(QtCore.Qt.AlignCenter)
            item_range_wtmax = QtGui.QTableWidgetItem(wtmax)
            item_range_wtmax.setTextAlignment(QtCore.Qt.AlignCenter)

            if led_status == '0':
                item_range_led = QtGui.QTableWidgetItem('OFF')
            else:
                item_range_led = QtGui.QTableWidgetItem('ON')
            item_range_led.setTextAlignment(QtCore.Qt.AlignCenter)

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
            addr_long_short = []
            addr_long_short.append((addr_long, addr_short))
            send_data = tmin + ',' + tmax + ',' + hmin + ',' + hmax + ',' + \
                    wtmin + ',' + wtmax + ',' + led_status
            self.ui_mainwindow.send_config_func(addr_long_short, send_data)
            print 'update_table_nodeinfo() send config to Arduino.'
            # Add new item.

        # table_plot_node display.
        item_plot_addr_long = QtGui.QTableWidgetItem(addr_long)
        item_plot_addr_long.setFlags(item_plot_addr_long.flags() & ~QtCore.Qt.ItemIsEditable)
        item_plot_addr_long.setTextAlignment(QtCore.Qt.AlignCenter)
        for item in self.ui_mainwindow.table_plot_node.findItems(addr_long, QtCore.Qt.MatchFixedString):
            # Item already exists, do not change.
            pass
            break
        else:    # Add new item.
            row = self.ui_mainwindow.table_plot_node.rowCount()
            self.ui_mainwindow.table_plot_node.setRowCount(row + 1)
            self.ui_mainwindow.table_plot_node.setItem(row, 0, item_plot_addr_long)

    def message_received(self, data):
        try:
            src_addr_long = data['source_addr_long']
            src_addr_short = data['source_addr']

            '''数据结构：字符串类型 '湿度，温度，水温' '''
            orig_str = data['rf_data']  # dict assign to string
            text = orig_str.split(',')
            self.update_table_nodeinfo((src_addr_long.encode('hex'), src_addr_short.encode('hex')), text)
            #self.update_database(src_addr_long.encode('hex'), text, database)
        except Exception, e:
            print e

    def run(self):
        self.refresh_table_timer.start(MONITOR_TIMER_DELAY)
        self.db_timer.start(5000)
        while not self.abort:
            #print 'xbee thread run.'
            try:
                if self.serial.isOpen() and self.serial.inWaiting():

                    data = self.xbee.wait_read_frame()
                    #print data
                    self.message_received(data)

                time.sleep(1)
            except KeyboardInterrupt:
                break
