# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_ConfigDialog.ui'
#
# Created: Sat Aug 16 20:57:07 2014
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

class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        ConfigDialog.setObjectName(_fromUtf8("ConfigDialog"))
        ConfigDialog.resize(378, 204)
        self.gridLayout = QtGui.QGridLayout(ConfigDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(195, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.pushButton_confirm = QtGui.QPushButton(ConfigDialog)
        self.pushButton_confirm.setObjectName(_fromUtf8("pushButton_confirm"))
        self.gridLayout.addWidget(self.pushButton_confirm, 1, 1, 1, 1)
        self.pushButton_discard = QtGui.QPushButton(ConfigDialog)
        self.pushButton_discard.setObjectName(_fromUtf8("pushButton_discard"))
        self.gridLayout.addWidget(self.pushButton_discard, 1, 2, 1, 1)
        self.groupBox = QtGui.QGroupBox(ConfigDialog)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 150))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        #self.timeEdit = QtGui.QTimeEdit(self.groupBox)
        self.timeEdit = QtGui.QTimeEdit(QtCore.QTime.currentTime(), self.groupBox)
        self.timeEdit.setMinimumSize(QtCore.QSize(100, 25))
        self.timeEdit.setDisplayFormat("HH:mm:ss")
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.horizontalLayout_2.addWidget(self.timeEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem2 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)

        self.dateEdit = QtGui.QDateEdit(QtCore.QDate.currentDate(), self.groupBox)
        #self.dateEdit = QtGui.QDateEdit(self.groupBox)
        self.dateEdit.setMinimumSize(QtCore.QSize(100, 25))
        self.dateEdit.setDisplayFormat("yyyy/MM/dd")
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.horizontalLayout_3.addWidget(self.dateEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)
        self.retranslateUi(ConfigDialog)
        QtCore.QObject.connect(self.pushButton_discard, QtCore.SIGNAL(_fromUtf8("clicked()")), ConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigDialog)

    def retranslateUi(self, ConfigDialog):
        ConfigDialog.setWindowTitle(_translate("ConfigDialog", "Dialog", None))
        self.pushButton_confirm.setText(_translate("ConfigDialog", "确认", None))
        self.pushButton_discard.setText(_translate("ConfigDialog", "取消", None))
        self.groupBox.setTitle(_translate("ConfigDialog", "时间日期设置", None))
        self.label.setText(_translate("ConfigDialog", "时间：", None))
        self.label_2.setText(_translate("ConfigDialog", "日期：", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ConfigDialog = QtGui.QDialog()
    ui = Ui_ConfigDialog()
    ui.setupUi(ConfigDialog)
    ConfigDialog.show()
    sys.exit(app.exec_())

