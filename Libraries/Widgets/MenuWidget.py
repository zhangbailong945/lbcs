from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QToolButton
from PyQt5.QtGui import QIcon,QPixmap

class MenuWidget(QWidget):

    def __init__(self,*args,**kwargs):
        super(MenuWidget,self).__init__(*args,**kwargs)
        self.setAttribute(Qt.WA_StyledBackground,True)
        self.initUI()
    
    def initUI(self):
        self.indexBtn=QToolButton(self)
        self.indexBtn.setText("首页")
        self.indexBtn.setObjectName("indexBtn")
        indexMap=QPixmap("./themes/default/images/logo.png")
        indexMap.width=50
        indexMap.height=50
        indexIcon=QIcon(indexMap)
        self.indexBtn.setIcon(indexIcon)
        self.indexBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.categoryBtn=QPushButton('分类',self,objectName="categoryBtn")
        self.categoryBtn.setIcon(QIcon("./themes/default/images/logo.png"))
        #按钮菜单，横向布局
        hlayout = QHBoxLayout(self, spacing=4)
        hlayout.setContentsMargins(10, 0, 10, 0)
        hlayout.addWidget(self.indexBtn)
        hlayout.addWidget(self.categoryBtn)
        hlayout.addStretch(1)

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
    w.show()
    sys.exit(app.exec_())