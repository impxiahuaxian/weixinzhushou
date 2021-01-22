# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import itchat


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        image = QtGui.QImage("./image/pexels-photo-3560451.jpeg")
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(image))

        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 200, 100, 50))
        self.pushButton.setObjectName("pushButton")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 100, 100, 100))
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "微信登陆界面"))
        self.pushButton.setText(_translate("MainWindow", "扫码登陆"))
        self.label.setText(_translate("MainWindow", " 登 陆 界 面"))
if __name__ == '__main__':
    ui = Ui_MainWindow()
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())


