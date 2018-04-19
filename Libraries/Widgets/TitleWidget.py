from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QSpacerItem,QSizePolicy,\
QPushButton,QLabel,QMenu
from PyQt5.QtGui import QIcon,QPixmap

class TitleWidget(QWidget):
    minimized=pyqtSignal()
    maximized=pyqtSignal()
    normaled=pyqtSignal()
    closed=pyqtSignal()

    def __init__(self,icon_visible=True,
        title_visible=True,
        skin_visible=True,
        min_visible=True,
        max_visible=False,
        nor_visible=False,
        close_visible=True,
        *args,**kwargs
        ):
        super(TitleWidget,self).__init__(*args,**kwargs)
        self.setAttribute(Qt.WA_StyledBackground,True)
        self.initUI(icon_visible,title_visible,skin_visible,min_visible,
        max_visible,nor_visible,close_visible
        )
    
    def showNormalBtn(self,visible):
        self._maximumButton.setVisible(not visible)
        self._normalButton.setVisible(visible)
    
    def initUI(self,icon_visible,title_visible,skin_visible,min_visible,max_visible,nor_visible,close_visible):
        layout = QHBoxLayout(self, spacing=10)
        layout.setContentsMargins(4, 0, 0, 0)
        '''标题栏-icon'''
        self.iconLabel=QLabel(self, objectName="iconLabel", visible=icon_visible)
        iconPmap=QPixmap("./themes/default/images/favicon.ico")
        iconPmap.width=30
        iconPmap.height=30
        self.iconLabel.setPixmap(iconPmap)
        
        layout.addWidget(self.iconLabel)
        '''标题栏-标题'''
        self.titleLabel=QLabel(self, objectName="titleLabel", visible=title_visible)
        self.titleLabel.setText("LoachBlog")
        layout.addWidget(self.titleLabel)
        # 左侧空白拉伸
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        '''标题栏-皮肤按钮'''
        skinMenu=QMenu(self)
        skinMenu.setObjectName("skinMenu")
        skinMenu.addAction("皮肤")
        skinMenu.addSeparator()
        skinMenu.addAction("默认经典")
        skinMenu.addAction("黑灯瞎火")
        skinMenu.addSeparator()
        skinMenu.addAction("版本检测")
        skinMenu.addAction("关于")
        self.skinBtn=QPushButton("", self, objectName="skinButton", visible=skin_visible)
        self.skinBtn.setMenu(skinMenu)
        self.skinBtn.setText("设置")
        self.skinBtn.setToolTip("设置")
        layout.addWidget(self.skinBtn)
        '''标题栏-最小化按钮'''
        self.miniBtn=QPushButton("", self, objectName="minimumButton", visible=min_visible, clicked=self.minimized.emit)
        self.miniBtn.setToolTip("最小化")
        layout.addWidget(self.miniBtn)
        '''标题栏-最大化按钮'''
        self._maximumButton = QPushButton(
            "", self, objectName="maximumButton", visible=max_visible, clicked=self.maximized.emit)
        self._maximumButton.setToolTip("最大化")
        layout.addWidget(self._maximumButton)
        '''标题栏-还原窗口'''
        self._normalButton = QPushButton(
            "", self, objectName="normalButton", visible=nor_visible, clicked=self.normaled.emit)
        self._normalButton.setToolTip("还原窗口")
        layout.addWidget(self._normalButton)
        '''标题栏-关闭按钮'''
        self.closeBtn=QPushButton("", self, objectName="closeButton", visible=close_visible, clicked=self.closed.emit)
        self.closeBtn.setToolTip("关闭")
        layout.addWidget(self.closeBtn)


if __name__=="__main__":
    import sys
    import os
    os.chdir("../../")
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFontDatabase
    app=QApplication(sys.argv)
    QFontDatabase.addApplicationFont("themes/default/fonts/default.ttf")
    app.setStyleSheet(open("themes/default/qss/default.qss","rb").read().decode("utf-8"))
    w=TitleWidget()
    w.show()
    sys.exit(app.exec_())

        