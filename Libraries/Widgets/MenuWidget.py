from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QPushButton,QHBoxLayout

class MenuWidget(QWidget):

    def __init__(self,*args,**kwargs):
        super(MenuWidget,self).__init__(*args,**kwargs)
        self.setAttribute(Qt.WA_StyledBackground,True)
    
    def initUI(self):
        self.IndexBtn=QPushButton('首页',self)
        self.CategoryBtn=QPushButton('分类',self)
        #按钮菜单，横向布局
        hlayout = QHBoxLayout(self, spacing=0)
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.addWidget(self.IndexBtn)
        hlayout.addWidget(self.CategoryBtn)

if __name__=="__main__":
    import sys
    import os
    os.chdir("../../")
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFontDatabase
    app=QApplication(sys.argv)
    QFontDatabase.addApplicationFont("themes/default/fonts/default.ttf")
    app.setStyleSheet(open("themes/default/qss/default.qss","rb").read().decode("utf-8"))
    w=MenuWidget()
    w.resize(800,55)
    w.show()
    sys.exit(app.exec_())