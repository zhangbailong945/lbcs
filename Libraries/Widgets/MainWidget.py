
from PyQt5.QtCore import Qt,QEvent,QPropertyAnimation,pyqtSignal,QRect,QEasingCurve,QParallelAnimationGroup
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout


from Libraries.Widgets.FramelessWindow import FramelessWindow
from Libraries.Widgets.TitleWidget import TitleWidget

__Author__="LoachBlog"
__Copyright="Copyright©2018 LoachBlog"
__Version__="1.0"

class MainWidget(QWidget):
    
    def __init__(self,*args,**kwargs):
        super(MainWidget,self).__init__(*args,**kwargs)
        self.resize(800,600)
        #QSS
        self.setAttribute(Qt.WA_StyledBackground,True)
        self.initUI()
    
    def initUI(self):
        '''自定义标题栏'''
        parent=self.parent or self.parentWidget() or self
        self._titleBar=TitleWidget(parent=self)
        self._titleBar.minimized.connect(parent.showMinimized)
        self._titleBar.maximized.connect(parent.showMaximized)
        self._titleBar.normaled.connect(parent.showNormal)
        self._titleBar.closed.connect(self.onClose)

        #总体布局
        layout=QVBoxLayout(self,spacing=0)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self._titleBar)

class MainWindow(FramelessWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(800, 600)
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