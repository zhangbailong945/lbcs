from PyQt5.QtCore import Qt,pyqtSignal,QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class IndexWidget(QWidget):

    def __init__(self,*args,**kwargs):
        super(IndexWidget,self).__init__(*args,**kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.initUI()
    
    def initUI(self):
        self.webView=QWebEngineView(self)
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.webView.load(QUrl("http://www.zhangbailong.com"))



if __name__ == "__main__":
    import sys
    import os
    os.chdir("../../")
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFontDatabase
    app=QApplication(sys.argv)
    QFontDatabase.addApplicationFont("themes/default/fonts/default.ttf")
    app.setStyleSheet(open("themes/default/qss/default.qss","rb").read().decode("utf-8"))
    w =IndexWidget()
    w.show()
    sys.exit(app.exec_())
