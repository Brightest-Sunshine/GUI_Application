# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\About.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(539, 444)
        self.label = QtWidgets.QLabel(About)
        self.label.setGeometry(QtCore.QRect(160, 100, 47, 13))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(About)
        self.pushButton.setGeometry(QtCore.QRect(220, 320, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "Form"))
        self.label.setText(_translate("About", "TextLabel"))
        self.pushButton.setText(_translate("About", "OK"))