
from PyQt5.QtCore import Qt,QEvent,QPropertyAnimation,pyqtSignal,QRect,QEasingCurve,QParallelAnimationGroup,QSize,QUrl
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QBoxLayout


from Libraries.Widgets.FramelessWindow import FramelessWindow
from Libraries.Widgets.TitleWidget import TitleWidget
from Libraries.Widgets.MenuWidget import MenuWidget
from Libraries.Widgets.ContentWidget import ContentWidget
from Libraries.Widgets.WebWidget import OAuthWindow
from Libraries.Widgets.IndexWidget import IndexWidget

__Author__="LoachBlog"
__Copyright="Copyright©2018 LoachBlog"
__Version__="1.0"

class MainWidget(QWidget):
    showed = pyqtSignal()
    closed = pyqtSignal()
    exited = pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super(MainWidget,self).__init__(*args,**kwargs)
        self.resize(800,600)
        #QSS
        self.setAttribute(Qt.WA_StyledBackground,True)
        self.initUI()
    
    def initUI(self):
        '''自定义标题栏'''
        parent = self.parent() or self.parentWidget() or self
        self._titleBar=TitleWidget(parent=self)
        self._titleBar.minimized.connect(parent.showMinimized)
        self._titleBar.maximized.connect(parent.showMaximized)
        self._titleBar.normaled.connect(parent.showNormal)
        self._titleBar.closed.connect(self.exited.emit)
        self._titleBar.setMaximumHeight(40)
        '''自定义菜单栏'''
        self._menuBar=MenuWidget(parent=self)
        self._menuBar.setMaximumHeight(80)
        
        #首页面板
        self._indexPanel=IndexWidget(parent=self)
        #中间内容布局
        #self._webBar=OAuthWindow(self)
        #总体布局,采用垂直布局
        layout=QVBoxLayout(self,spacing=0)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self._titleBar)
        layout.addWidget(self._menuBar)
        #layout.addWidget(self._webBar)
        layout.addWidget(self._indexPanel)
        self.setLayout(layout)
    

class MainWindow(FramelessWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(800,500)
        layout=QVBoxLayout(self,spacing=0)
        layout.setContentsMargins(0,0,0,0)
        self._mainWidget=MainWidget(self)
        self._mainWidget.exited.connect(self.close)
        layout.addWidget(self._mainWidget)
        


if __name__=="__main__":
    import sys
    import os
    os.chdir("../../")
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFontDatabase
    app=QApplication(sys.argv)
    QFontDatabase.addApplicationFont("themes/default/fonts/default.ttf")
    app.setStyleSheet(open("themes/default/qss/default.qss","rb").read().decode("utf-8"))
    w=MainWindow()
    w.show()
    sys.exit(app.exec_())