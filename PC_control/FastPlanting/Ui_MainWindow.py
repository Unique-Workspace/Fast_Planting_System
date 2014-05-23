# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_MainWindow.ui'
#
# Created: Fri May 23 21:30:37 2014
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
        MainWindow.resize(904, 726)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.editorBox = QtGui.QGroupBox(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editorBox.sizePolicy().hasHeightForWidth())
        self.editorBox.setSizePolicy(sizePolicy)
        self.editorBox.setMaximumSize(QtCore.QSize(280, 16777215))
        self.editorBox.setObjectName(_fromUtf8("editorBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.editorBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.listNodeWidget = QtGui.QListWidget(self.editorBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listNodeWidget.sizePolicy().hasHeightForWidth())
        self.listNodeWidget.setSizePolicy(sizePolicy)
        self.listNodeWidget.setObjectName(_fromUtf8("listNodeWidget"))
        self.verticalLayout_2.addWidget(self.listNodeWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.button_open_serial = QtGui.QPushButton(self.editorBox)
        self.button_open_serial.setObjectName(_fromUtf8("button_open_serial"))
        self.horizontalLayout.addWidget(self.button_open_serial)
        self.button_scan = QtGui.QPushButton(self.editorBox)
        self.button_scan.setCheckable(True)
        self.button_scan.setObjectName(_fromUtf8("button_scan"))
        self.horizontalLayout.addWidget(self.button_scan)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.previewerBox = QtGui.QGroupBox(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewerBox.sizePolicy().hasHeightForWidth())
        self.previewerBox.setSizePolicy(sizePolicy)
        self.previewerBox.setObjectName(_fromUtf8("previewerBox"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.previewerBox)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.columnView = QtGui.QColumnView(self.previewerBox)
        self.columnView.setObjectName(_fromUtf8("columnView"))
        self.horizontalLayout_3.addWidget(self.columnView)
        self.horizontalLayout_4.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 904, 23))
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
        QtCore.QObject.connect(self.menu_exit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.editorBox.setTitle(_translate("MainWindow", "节点列表", None))
        self.button_open_serial.setText(_translate("MainWindow", "连接", None))
        self.button_scan.setText(_translate("MainWindow", "扫描", None))
        self.previewerBox.setTitle(_translate("MainWindow", "节点信息", None))
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

