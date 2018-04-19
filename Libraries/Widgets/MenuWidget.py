from PyQt5.QtCore import Qt,QSize
from PyQt5.QtWidgets import QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QToolButton
from PyQt5.QtGui import QIcon,QPixmap

class MenuWidget(QWidget):

    def __init__(self,*args,**kwargs):
        super(MenuWidget,self).__init__(*args,**kwargs)
        self.setAttribute(Qt.WA_StyledBackground,True)
        self.initUI()
    
    def initUI(self):
        '''菜单-首页按钮'''
        self.indexBtn=QToolButton(self)
        self.indexBtn.setText("首页")
        self.indexBtn.setObjectName("indexBtn")
        indexMap=QPixmap("./themes/default/images/logo.png")
        indexMap.width=50
        indexMap.height=50
        indexIcon=QIcon(indexMap)
        self.indexBtn.setIconSize(QSize(50,50))
        self.indexBtn.setIcon(indexIcon)
        self.indexBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        '''菜单-分类按钮'''
        self.categoryBtn=QToolButton(self)
        self.categoryBtn.setText("分类")
        self.categoryBtn.setObjectName("categoryBtn")
        categoryMap=QPixmap("./themes/default/images/category.png")
        categoryMap.width=50
        categoryMap.height=50
        categoryIcon=QIcon(categoryMap)
        self.categoryBtn.setIconSize(QSize(50,50))
        self.categoryBtn.setIcon(categoryIcon)
        self.categoryBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #按钮菜单，横向布局
        hlayout = QHBoxLayout(self, spacing=4)
        hlayout.setContentsMargins(10,0,0, 0)
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