from PyQt5 import QtCore, QtGui, QtWidgets
from UI_Main import *
from WeChatBot import *
class show(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):

        super(show, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.wechat_run)

    def wechat_run(self):
        itchat.auto_login()
        info().scheduler()
        # search_male()
        itchat.run()

if __name__ == "__main__":
    #ui = Ui_MainWindow()
    app = QtWidgets.QApplication(sys.argv)
    #widget = QtWidgets.QMainWindow()
    wechat = show()
    wechat.show()
    sys.exit(app.exec_())