from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QWidget

class IndexWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super(IndexWidget,self).__init__(*args,**kwargs)
        # 保证qss有效
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.initUI()
    
    def initUI(self):
        self.resize(800,400)

if __name__ == "__main__":
    import sys
    import os
    os.chdir("../../")
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFontDatabase
    app=QApplication(sys.argv)
    QFontDatabase.addApplicationFont("themes/default/fonts/default.ttf")
    app.setStyleSheet(open("themes/default/qss/default.qss","rb").read().decode("utf-8"))
    w = IndexWidget()
    w.show()
    sys.exit(app.exec_())
