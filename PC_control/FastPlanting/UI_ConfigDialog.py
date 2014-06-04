# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_ConfigDialog.ui'
#
# Created: Wed Jun  4 23:53:11 2014
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
        ConfigDialog.resize(350, 200)
        self.gridLayout_2 = QtGui.QGridLayout(ConfigDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(ConfigDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinBox_tmin = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_tmin.sizePolicy().hasHeightForWidth())
        self.spinBox_tmin.setSizePolicy(sizePolicy)
        self.spinBox_tmin.setMinimumSize(QtCore.QSize(50, 28))
        self.spinBox_tmin.setDecimals(1)
        self.spinBox_tmin.setObjectName(_fromUtf8("spinBox_tmin"))
        self.gridLayout.addWidget(self.spinBox_tmin, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.spinBox_tmax = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBox_tmax.setMinimumSize(QtCore.QSize(0, 28))
        self.spinBox_tmax.setDecimals(1)
        self.spinBox_tmax.setObjectName(_fromUtf8("spinBox_tmax"))
        self.gridLayout.addWidget(self.spinBox_tmax, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBox_hmin = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBox_hmin.setMinimumSize(QtCore.QSize(0, 28))
        self.spinBox_hmin.setDecimals(1)
        self.spinBox_hmin.setObjectName(_fromUtf8("spinBox_hmin"))
        self.gridLayout.addWidget(self.spinBox_hmin, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)
        self.spinBox_hmax = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBox_hmax.setMinimumSize(QtCore.QSize(0, 28))
        self.spinBox_hmax.setDecimals(1)
        self.spinBox_hmax.setObjectName(_fromUtf8("spinBox_hmax"))
        self.gridLayout.addWidget(self.spinBox_hmax, 1, 3, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.spinBox_wtmin = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBox_wtmin.setMinimumSize(QtCore.QSize(0, 28))
        self.spinBox_wtmin.setDecimals(1)
        self.spinBox_wtmin.setObjectName(_fromUtf8("spinBox_wtmin"))
        self.gridLayout.addWidget(self.spinBox_wtmin, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)
        self.spinBox_wtmax = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBox_wtmax.setMinimumSize(QtCore.QSize(0, 28))
        self.spinBox_wtmax.setDecimals(1)
        self.spinBox_wtmax.setObjectName(_fromUtf8("spinBox_wtmax"))
        self.gridLayout.addWidget(self.spinBox_wtmax, 2, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.radioBtn_openLed = QtGui.QRadioButton(self.groupBox)
        self.radioBtn_openLed.setIconSize(QtCore.QSize(20, 20))
        self.radioBtn_openLed.setObjectName(_fromUtf8("radioBtn_openLed"))
        self.gridLayout.addWidget(self.radioBtn_openLed, 3, 1, 1, 1)
        self.radioBtn_closeLed = QtGui.QRadioButton(self.groupBox)
        self.radioBtn_closeLed.setIconSize(QtCore.QSize(20, 20))
        self.radioBtn_closeLed.setObjectName(_fromUtf8("radioBtn_closeLed"))
        self.gridLayout.addWidget(self.radioBtn_closeLed, 3, 2, 1, 2)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_config = QtGui.QPushButton(ConfigDialog)
        self.pushButton_config.setObjectName(_fromUtf8("pushButton_config"))
        self.horizontalLayout.addWidget(self.pushButton_config)
        self.pushButton_close = QtGui.QPushButton(ConfigDialog)
        self.pushButton_close.setObjectName(_fromUtf8("pushButton_close"))
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(ConfigDialog)
        QtCore.QMetaObject.connectSlotsByName(ConfigDialog)

    def retranslateUi(self, ConfigDialog):
        ConfigDialog.setWindowTitle(_translate("ConfigDialog", "Dialog", None))
        self.groupBox.setTitle(_translate("ConfigDialog", "GroupBox", None))
        self.label.setText(_translate("ConfigDialog", "室温范围：", None))
        self.label_5.setText(_translate("ConfigDialog", "---", None))
        self.label_2.setText(_translate("ConfigDialog", "湿度范围：", None))
        self.label_6.setText(_translate("ConfigDialog", "---", None))
        self.label_3.setText(_translate("ConfigDialog", "水温范围：", None))
        self.label_7.setText(_translate("ConfigDialog", "---", None))
        self.label_4.setText(_translate("ConfigDialog", "LED灯：", None))
        self.radioBtn_openLed.setText(_translate("ConfigDialog", "打开", None))
        self.radioBtn_closeLed.setText(_translate("ConfigDialog", "关闭", None))
        self.pushButton_config.setText(_translate("ConfigDialog", "设置", None))
        self.pushButton_close.setText(_translate("ConfigDialog", "关闭", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ConfigDialog = QtGui.QDialog()
    ui = Ui_ConfigDialog()
    ui.setupUi(ConfigDialog)
    ConfigDialog.show()
    sys.exit(app.exec_())

