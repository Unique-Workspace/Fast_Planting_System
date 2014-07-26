#! /usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from database import RecordDb

TROOM = 'TRoom'
TWATER = 'Twater'
HUMIDITY = 'Humidity'

ONE_MINUTE = 60  # test
TEN_MINUTES = (10*ONE_MINUTE)
THIRTY_MINUTES = (30*ONE_MINUTE)
ONE_HOUR = (60*ONE_MINUTE)
THREE_HOURS = (3*ONE_HOUR)
SIX_HOURS = (6*ONE_HOUR)
TWELVE_HOURS = (12*ONE_HOUR)
ONE_DAY = (24*ONE_HOUR)
THREE_DAYS = (3*ONE_DAY)
SEVEN_DAYS = (7*ONE_DAY)
ONE_MONTH = (30*ONE_DAY)
ALL_TIME_STATIC = 0
MONITOR_DELAY_TIME = 5000
MONITOR_DELAY_SECOND = (MONITOR_DELAY_TIME/1000)

global_plot_time_base = QtCore.QDateTime.currentDateTime()


# 曲线显示时间轴
class TimeScaleDraw(Qwt.QwtScaleDraw):

    def __init__(self, base_time, *args):
        Qwt.QwtScaleDraw.__init__(self, *args)
        self.base_time = base_time

    # __init__()

    def label(self, value):
        up_time = self.base_time.addSecs(int(value))
        return Qwt.QwtText(up_time.toString())

    # label()

# class TimeScaleDraw


class Background(Qwt.QwtPlotItem):

    def __init__(self):
        Qwt.QwtPlotItem.__init__(self)
        self.setZ(0.0)

    # __init__()

    def rtti(self):
        return Qwt.QwtPlotItem.Rtti_PlotUserItem

    # rtti()

    def draw(self, painter, xMap, yMap, rect):
        c = QtGui.QColor(QtCore.Qt.white)
        r = QtCore.QRect(rect)

        for i in range(100, 0, -10):
            r.setBottom(yMap.transform(i - 10))
            r.setTop(yMap.transform(i))
            painter.fillRect(r, c)
            c = c.dark(110)
    # draw()
#  class Background


# reload class QwtPlotPicker for time scale display.
class PlotPickerByTime(Qwt.QwtPlotPicker):
    def __init__(self,  *args):
        Qwt.QwtPlotPicker.__init__(self, *args)

    def trackerTextF(self, pos):
        time = self.toDateTime(float(pos.x()))
        y = '%.2f' % float(pos.y())
        text = time.toString('MM-dd hh:mm:ss') + ', ' + y

        return Qwt.QwtText(text)

    def toDateTime(self, value):
        global global_plot_time_base
        value *= 1000
        time = global_plot_time_base.addMSecs(value)
        return time


# 曲线显示类
class PlotDisplay(Qwt.QwtPlot):
    def __init__(self, qwt_plot, time_limit_index):
        super(PlotDisplay, self).__init__()

        self.curves = {}
        self.curve_data = {}
        self.time_data = []
        self.time_limit = self.get_plot_time_limit(time_limit_index)
        self.base_msec = 0
        self.current_msec = QtCore.QDateTime.currentMSecsSinceEpoch()
        self.selected_plot_node = {}
        self.start_time = 0
        # alias
        font = self.fontInfo().family()

        self.qwtPlot = qwt_plot
        text = Qwt.QwtText(u'水温[C\u00b0]')
        text.setColor(QtCore.Qt.blue)
        text.setFont(QtGui.QFont(font, 12, QtGui.QFont.Bold))
        self.qwtPlot.setTitle(text)
        # axes
        self.qwtPlot.enableAxis(Qwt.QwtPlot.yRight)
        text = Qwt.QwtText(u'温度[C\u00b0]')
        text.setColor(QtCore.Qt.red)
        text.setFont(QtGui.QFont(font, 12, QtGui.QFont.Bold))
        self.qwtPlot.setAxisTitle(Qwt.QwtPlot.yLeft, text)
        text = Qwt.QwtText(u'湿度 [\u00b0]')
        text.setColor(QtCore.Qt.darkGreen)
        text.setFont(QtGui.QFont(font, 12, QtGui.QFont.Bold))
        self.qwtPlot.setAxisTitle(Qwt.QwtPlot.yRight, text)
        self.qwtPlot.setAxisScale(Qwt.QwtPlot.yLeft, 0, 100)
        self.qwtPlot.setAxisScale(Qwt.QwtPlot.yRight, 0, 100)
        self.qwtPlot.setCanvasBackground(QtCore.Qt.white)

        #self.qwtPlot.setAxisTitle(Qwt.QwtPlot.xBottom, u'日期时间')
        #self.qwtPlot.setAxisScale(Qwt.QwtPlot.xBottom, 0, 60)
        date_time = QtCore.QDateTime.currentDateTime()
        self.qwtPlot.setAxisScaleDraw(
            Qwt.QwtPlot.xBottom, TimeScaleDraw(date_time))
        self.qwtPlot.setAxisLabelRotation(Qwt.QwtPlot.xBottom, -60.0)
        self.qwtPlot.setAxisLabelAlignment(
            Qwt.QwtPlot.xBottom, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.first_update_flag = True

        grid = Qwt.QwtPlotGrid()
        grid.attach(self.qwtPlot)
        grid.setPen(QtGui.QPen(QtCore.Qt.black, 0, QtCore.Qt.DotLine))

        self.picker = PlotPickerByTime(
            Qwt.QwtPlot.xBottom,
            Qwt.QwtPlot.yLeft,
            Qwt.QwtPicker.PointSelection | Qwt.QwtPicker.DragSelection,
            Qwt.QwtPlotPicker.CrossRubberBand,
            Qwt.QwtPicker.AlwaysOn,
            self.qwtPlot.canvas())
        self.picker.setRubberBandPen(QtGui.QPen(QtCore.Qt.yellow))
        self.picker.setTrackerPen(QtGui.QPen(QtCore.Qt.cyan))
        #zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
        #                       Qwt.QwtPlot.yLeft,
        #                       Qwt.QwtPicker.DragSelection,
        #                       Qwt.QwtPicker.AlwaysOff,
        #                       self.qwtPlot.canvas())
        #zoomer.setRubberBandPen(QtGui.QPen(QtCore.Qt.darkGray))

        curve = Qwt.QwtPlotCurve('Temperature Room')
        curve.setPen(QtGui.QPen(QtCore.Qt.red))
        curve.attach(self.qwtPlot)
        self.curves[TROOM] = curve
        self.curve_data[TROOM] = []

        curve = Qwt.QwtPlotCurve('Humidity')
        curve.setPen(QtGui.QPen(QtCore.Qt.darkGreen))
        curve.attach(self.qwtPlot)
        self.curves[HUMIDITY] = curve
        self.curve_data[HUMIDITY] = []

        curve = Qwt.QwtPlotCurve('Temperature Water')
        curve.setPen(QtGui.QPen(QtCore.Qt.blue))
        curve.attach(self.qwtPlot)
        self.curves[TWATER] = curve
        self.curve_data[TWATER] = []

        self.qwtPlot.setAutoReplot(False)
        self.qwtPlot.plotLayout().setAlignCanvasToScales(True)
        background = Background()
        background.attach(self.qwtPlot)
        
        self.connect(self.picker,
                     QtCore.SIGNAL('moved(const QPoint &)'),
                     self.moved)
        self.connect(self.picker,
                     QtCore.SIGNAL('selected(const QPolygon &)'),
                     self.selected)

    def showInfo(self, text=None):
        print 'plot showInfo'
        if not text:
            if self.picker.rubberBand():
                text = 'Cursor Pos: Press left mouse button in plot region'
            else:
                text = 'Zoom: Press mouse button and drag'
                
    # showInfo()
    
    def moved(self, point):
        print 'plot moved x=' + str(point.x()) + ' y=' + str(point.y())
        info = "Freq=%g, Ampl=%g, Phase=%g" % (
            self.qwtPlot.invTransform(Qwt.QwtPlot.xBottom, point.x()),
            self.qwtPlot.invTransform(Qwt.QwtPlot.yLeft, point.y()),
            self.qwtPlot.invTransform(Qwt.QwtPlot.yRight, point.y()))
        self.showInfo(info)

    # moved()

    def selected(self, _):
        print 'plot selected'
        self.showInfo()

    # selected()
    
    def update_plot(self, sensor_data):
        if self.first_update_flag:
            date_time = QtCore.QDateTime.currentDateTime()
            global global_plot_time_base
            global_plot_time_base = date_time
            self.qwtPlot.setAxisScaleDraw(
                Qwt.QwtPlot.xBottom, TimeScaleDraw(date_time))
            self.qwtPlot.setAxisLabelRotation(Qwt.QwtPlot.xBottom, -60.0)
            self.qwtPlot.setAxisLabelAlignment(
                Qwt.QwtPlot.xBottom, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
            self.first_update_flag = False

        if (self.time_limit/MONITOR_DELAY_SECOND) > len(self.time_data):
            self.current_msec = QtCore.QDateTime.currentMSecsSinceEpoch()
            time = (self.current_msec - self.base_msec) / 1000

            for key in self.curve_data.keys():
                self.curve_data[key].append(sensor_data[key])
            self.time_data.append(time)
        else:
            for i in xrange(0, len(self.time_data)):
                self.time_data[i] += MONITOR_DELAY_SECOND
            for key in self.curve_data.keys():
                self.curve_data[key][0:-1] = self.curve_data[key][1:]
                self.curve_data[key][-1] = sensor_data[key]

        #print len(self.time_data), self.time_data[0], self.time_data[-1]
        #print self.time_data
        self.setAxisScale(
                Qwt.QwtPlot.xBottom, self.time_data[0], self.time_data[-1])
        for key in self.curves.keys():
            self.curves[key].setData(self.time_data, self.curve_data[key])
        self.qwtPlot.replot()

    @staticmethod
    def calculate_time_range(time_limit):
        time_range = {}
        end = QtCore.QDateTime.currentDateTime()
        start = end.addSecs(-time_limit)
        time_range['end'] = str(end.toString('yyyy-MM-dd hh:mm:ss'))
        time_range['start'] = str(start.toString('yyyy-MM-dd hh:mm:ss'))
        global global_plot_time_base
        global_plot_time_base = start
        return time_range

    # 测试指定时间范围内有没有节点信息
    def test_node_db_info(self, time_limit):
        database = RecordDb()
        if time_limit == ALL_TIME_STATIC:
            node_data = database.curve_data_read(self.selected_plot_node['text'])
        else:
            time_range = self.calculate_time_range(time_limit)
            node_data = database.curve_data_read(self.selected_plot_node['text'], time_range['start'], time_range['end'])
        database.do_close()
        return len(node_data)

    # 从数据库读取节点信息，读完关闭
    def read_node_db_info(self, time_limit):
        times = []
        database = RecordDb()
        if time_limit == ALL_TIME_STATIC:
            node_data = database.curve_data_read(self.selected_plot_node['text'])
        else:
            time_range = self.calculate_time_range(time_limit)
            node_data = database.curve_data_read(self.selected_plot_node['text'], time_range['start'], time_range['end'])
        database.do_close()
        self.clean_plot()   # 清除curve_data{}字典
        if len(node_data) == 0:  # 在指定范围内有数据,才会去更新
            return -1
        # 时间，温度，湿度，水温
        for data in node_data:
            times.append(data[0])
            self.curve_data[TROOM].append(data[1])
            self.curve_data[HUMIDITY].append(data[2])
            self.curve_data[TWATER].append(data[3])
        self.start_time = QtCore.QDateTime.fromString(times[0], 'yyyy-MM-dd hh:mm:ss')  # start time for static display.
        start_sec = self.start_time.toMSecsSinceEpoch() / 1000.0
        if self.base_msec == 0:
            self.base_msec = self.start_time.toMSecsSinceEpoch()
        for time in times:
            time = QtCore.QDateTime.fromString(time, 'yyyy-MM-dd hh:mm:ss')
            current_sec = time.toMSecsSinceEpoch() / 1000.0
            current_sec -= start_sec
            self.time_data.append(current_sec)
        #print len(self.time_data), self.time_data
        #print self.time_data[0], self.time_data[-1], len(self.time_data)
        #print (self.time_data[-1] - self.time_data[0]) / 3600/24

    # 绘制time_limit时限的静态图表
    def draw_time_limit_plot(self, time_limit):
        ret = self.read_node_db_info(time_limit)
        if ret == -1:
            print 'draw_time_limit_plot() ret -1'
            return
        self.qwtPlot.setAxisScaleDraw(
                Qwt.QwtPlot.xBottom, TimeScaleDraw(self.start_time))
        self.qwtPlot.setAxisLabelRotation(Qwt.QwtPlot.xBottom, -60.0)
        self.qwtPlot.setAxisLabelAlignment(
            Qwt.QwtPlot.xBottom, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.first_update_flag = False
        self.setAxisScale(
                Qwt.QwtPlot.xBottom, self.time_data[0], self.time_data[-1])
        for key in self.curves.keys():
            self.curves[key].setData(self.time_data, self.curve_data[key])
        self.qwtPlot.replot()

    # 根据选择的时限，重绘曲线。
    def redraw_plot(self, time_sec_limit):
        # 重绘time_limit期间的曲线：
        # 1、清空curve_data数据
        # 2、从数据库读取time_limit期间的数据，并存入curve_data
        # 3、重绘图表，完成。交给plot_timer_event在此基础上继续刷新。
        #print time_sec_limit
        self.time_limit = time_sec_limit
        self.draw_time_limit_plot(time_sec_limit)

    def clean_plot(self):
        # 清空所有本地数据
        for key in self.curve_data.keys():
            self.curve_data[key] = []
        self.time_data = []
        for key in self.curves.keys():
            self.curves[key].setData(self.time_data, self.curve_data[key])

        self.qwtPlot.replot()
        self.base_msec = 0
        self.first_update_flag = True
        #print 'PlotDisplay.clean_plot()'

    @staticmethod
    def get_plot_time_limit(selected_index):
        time_limit = 0
        if selected_index == 7:
            time_limit = ALL_TIME_STATIC
        elif selected_index == 0:
            time_limit = ONE_MINUTE
        elif selected_index == 1:
            time_limit = THIRTY_MINUTES
        elif selected_index == 2:
            time_limit = ONE_HOUR
        elif selected_index == 3:
            time_limit = SIX_HOURS
        elif selected_index == 4:
            time_limit = ONE_DAY
        elif selected_index == 5:
            time_limit = SEVEN_DAYS
        elif selected_index == 6:
            time_limit = ONE_MONTH
        else:
            pass
        return time_limit
# class PlotDisplay
