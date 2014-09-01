# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_SerialDialog.ui'
#
# Created: Tue Sep 02 00:03:14 2014
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

class Ui_SerialDialog(object):
    def setupUi(self, SerialDialog):
        SerialDialog.setObjectName(_fromUtf8("SerialDialog"))
        SerialDialog.resize(380, 160)
        self.gridLayout_3 = QtGui.QGridLayout(SerialDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(SerialDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_Serial = QtGui.QComboBox(self.groupBox)
        self.comboBox_Serial.setEditable(True)
        self.comboBox_Serial.setObjectName(_fromUtf8("comboBox_Serial"))
        self.comboBox_Serial.addItem(_fromUtf8(""))
        self.comboBox_Serial.addItem(_fromUtf8(""))
        self.comboBox_Serial.addItem(_fromUtf8(""))
        self.comboBox_Serial.addItem(_fromUtf8(""))
        self.comboBox_Serial.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_Serial)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox_BaundRate = QtGui.QComboBox(self.groupBox)
        self.comboBox_BaundRate.setEditable(True)
        self.comboBox_BaundRate.setObjectName(_fromUtf8("comboBox_BaundRate"))
        self.comboBox_BaundRate.addItem(_fromUtf8(""))
        self.comboBox_BaundRate.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBox_BaundRate)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pushButton_confirm = QtGui.QPushButton(SerialDialog)
        self.pushButton_confirm.setObjectName(_fromUtf8("pushButton_confirm"))
        self.horizontalLayout_3.addWidget(self.pushButton_confirm)
        self.pushButton_discard = QtGui.QPushButton(SerialDialog)
        self.pushButton_discard.setObjectName(_fromUtf8("pushButton_discard"))
        self.horizontalLayout_3.addWidget(self.pushButton_discard)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.retranslateUi(SerialDialog)
        QtCore.QObject.connect(self.pushButton_discard, QtCore.SIGNAL(_fromUtf8("clicked()")), SerialDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SerialDialog)

    def retranslateUi(self, SerialDialog):
        SerialDialog.setWindowTitle(_translate("SerialDialog", "串口", None))
        self.groupBox.setTitle(_translate("SerialDialog", "串口配置", None))
        self.label.setText(_translate("SerialDialog", "串口号：", None))
        self.comboBox_Serial.setItemText(0, _translate("SerialDialog", "/dev/ttyAMA0", None))
        self.comboBox_Serial.setItemText(1, _translate("SerialDialog", "COM1", None))
        self.comboBox_Serial.setItemText(2, _translate("SerialDialog", "COM2", None))
        self.comboBox_Serial.setItemText(3, _translate("SerialDialog", "COM26", None))
        self.comboBox_Serial.setItemText(4, _translate("SerialDialog", "COM28", None))
        self.label_2.setText(_translate("SerialDialog", "波特率：", None))
        self.comboBox_BaundRate.setItemText(0, _translate("SerialDialog", "115200", None))
        self.comboBox_BaundRate.setItemText(1, _translate("SerialDialog", "9600", None))
        self.pushButton_confirm.setText(_translate("SerialDialog", "确认", None))
        self.pushButton_discard.setText(_translate("SerialDialog", "取消", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SerialDialog = QtGui.QDialog()
    ui = Ui_SerialDialog()
    ui.setupUi(SerialDialog)
    SerialDialog.show()
    sys.exit(app.exec_())

