# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_MainWindow.ui'
#
# Created: Sat Jun 07 17:59:47 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(914, 698)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tab_display = QtGui.QTabWidget(self.centralwidget)
        self.tab_display.setObjectName(_fromUtf8("tab_display"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.previewerBox = QtGui.QGroupBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewerBox.sizePolicy().hasHeightForWidth())
        self.previewerBox.setSizePolicy(sizePolicy)
        self.previewerBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.previewerBox.setObjectName(_fromUtf8("previewerBox"))
        self.gridLayout = QtGui.QGridLayout(self.previewerBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.table_node_info = QtGui.QTableWidget(self.previewerBox)
        self.table_node_info.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_node_info.setColumnCount(0)
        self.table_node_info.setObjectName(_fromUtf8("table_node_info"))
        self.table_node_info.setRowCount(0)
        self.gridLayout.addWidget(self.table_node_info, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.previewerBox)
        self.groupBox = QtGui.QGroupBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(280, 16777215))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.timeEdit = QtGui.QTimeEdit(self.groupBox)
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.verticalLayout.addWidget(self.timeEdit)
        self.dateEdit = QtGui.QDateEdit(self.groupBox)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.verticalLayout.addWidget(self.dateEdit)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.plainTextEdit = QtGui.QPlainTextEdit(self.groupBox)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.splitter = QtGui.QSplitter(self.groupBox)
        self.splitter.setMinimumSize(QtCore.QSize(0, 50))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.button_config = QtGui.QPushButton(self.splitter)
        self.button_config.setCheckable(False)
        self.button_config.setObjectName(_fromUtf8("button_config"))
        self.button_open_serial = QtGui.QPushButton(self.splitter)
        self.button_open_serial.setObjectName(_fromUtf8("button_open_serial"))
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.tab_display.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.table_range_display = QtGui.QTableWidget(self.groupBox_2)
        self.table_range_display.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.table_range_display.setObjectName(_fromUtf8("table_range_display"))
        self.table_range_display.setColumnCount(0)
        self.table_range_display.setRowCount(0)
        self.verticalLayout_2.addWidget(self.table_range_display)
        self.splitter_2 = QtGui.QSplitter(self.groupBox_2)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.label_3 = QtGui.QLabel(self.splitter_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.line_config_status = QtGui.QLineEdit(self.splitter_2)
        self.line_config_status.setObjectName(_fromUtf8("line_config_status"))
        self.pushButton_config = QtGui.QPushButton(self.splitter_2)
        self.pushButton_config.setObjectName(_fromUtf8("pushButton_config"))
        self.pushButton_save = QtGui.QPushButton(self.splitter_2)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.verticalLayout_2.addWidget(self.splitter_2)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.tab_display.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tab_display)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 914, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        self.menu_3 = QtGui.QMenu(self.menubar)
        self.menu_3.setObjectName(_fromUtf8("menu_3"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName(_fromUtf8("action"))
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName(_fromUtf8("action_2"))
        self.action_3 = QtGui.QAction(MainWindow)
        self.action_3.setObjectName(_fromUtf8("action_3"))
        self.action_scan_node = QtGui.QAction(MainWindow)
        self.action_scan_node.setObjectName(_fromUtf8("action_scan_node"))
        self.action_5 = QtGui.QAction(MainWindow)
        self.action_5.setObjectName(_fromUtf8("action_5"))
        self.action_7 = QtGui.QAction(MainWindow)
        self.action_7.setObjectName(_fromUtf8("action_7"))
        self.action_8 = QtGui.QAction(MainWindow)
        self.action_8.setObjectName(_fromUtf8("action_8"))
        self.menu_exit = QtGui.QAction(MainWindow)
        self.menu_exit.setObjectName(_fromUtf8("menu_exit"))
        self.action_10 = QtGui.QAction(MainWindow)
        self.action_10.setObjectName(_fromUtf8("action_10"))
        self.action_11 = QtGui.QAction(MainWindow)
        self.action_11.setObjectName(_fromUtf8("action_11"))
        self.menu_config_serial = QtGui.QAction(MainWindow)
        self.menu_config_serial.setObjectName(_fromUtf8("menu_config_serial"))
        self.menu.addAction(self.menu_config_serial)
        self.menu.addAction(self.action_scan_node)
        self.menu.addAction(self.action_5)
        self.menu.addSeparator()
        self.menu.addAction(self.action_7)
        self.menu.addAction(self.action_8)
        self.menu.addAction(self.menu_exit)
        self.menu_2.addAction(self.action_3)
        self.menu_2.addAction(self.action_10)
        self.menu_2.addAction(self.action_11)
        self.menu_3.addAction(self.action)
        self.menu_3.addAction(self.action_2)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        self.tab_display.setCurrentIndex(0)
        QtCore.QObject.connect(self.menu_exit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.previewerBox.setTitle(_translate("MainWindow", "节点信息", None))
        self.groupBox.setTitle(_translate("MainWindow", "控制", None))
        self.label_2.setText(_translate("MainWindow", "时间日期：", None))
        self.label.setText(_translate("MainWindow", "提醒：", None))
        self.button_config.setText(_translate("MainWindow", "配置", None))
        self.button_open_serial.setText(_translate("MainWindow", "连接", None))
        self.tab_display.setTabText(self.tab_display.indexOf(self.tab), _translate("MainWindow", "显示", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "范围显示", None))
        self.label_3.setText(_translate("MainWindow", "信息显示：", None))
        self.pushButton_config.setText(_translate("MainWindow", "设置生效", None))
        self.pushButton_save.setText(_translate("MainWindow", "保存参数", None))
        self.tab_display.setTabText(self.tab_display.indexOf(self.tab_2), _translate("MainWindow", "设置", None))
        self.menu.setTitle(_translate("MainWindow", "操作", None))
        self.menu_2.setTitle(_translate("MainWindow", "视图", None))
        self.menu_3.setTitle(_translate("MainWindow", "帮助", None))
        self.action.setText(_translate("MainWindow", "调试", None))
        self.action_2.setText(_translate("MainWindow", "关于", None))
        self.action_3.setText(_translate("MainWindow", "查看全部", None))
        self.action_scan_node.setText(_translate("MainWindow", "扫描节点", None))
        self.action_5.setText(_translate("MainWindow", "增加节点", None))
        self.action_7.setText(_translate("MainWindow", "保存配置", None))
        self.action_8.setText(_translate("MainWindow", "配置另存为", None))
        self.menu_exit.setText(_translate("MainWindow", "退出", None))
        self.action_10.setText(_translate("MainWindow", "单独查看", None))
        self.action_11.setText(_translate("MainWindow", "曲线视图", None))
        self.menu_config_serial.setText(_translate("MainWindow", "配置串口", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

