from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QSpacerItem,QSizePolicy,\
QPushButton,QLabel
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
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.iconLabel=QLabel(self, objectName="iconLabel", visible=icon_visible)
        self.iconLabel.setPicture
        layout.addWidget(self.iconLabel)
        self.titleLabel=QLabel(self, objectName="titleLabel", visible=title_visible)
        self.titleLabel.setText("这里是标题")
        layout.addWidget(self.titleLabel)
        # 左侧空白拉伸
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(QPushButton(
            "", self, objectName="skinButton", visible=skin_visible))
        layout.addWidget(QPushButton(
            "", self, objectName="minimumButton", visible=min_visible, clicked=self.minimized.emit))
        self._maximumButton = QPushButton(
            "", self, objectName="maximumButton", visible=max_visible, clicked=self.maximized.emit)
        layout.addWidget(self._maximumButton)
        self._normalButton = QPushButton(
            "", self, objectName="normalButton", visible=nor_visible, clicked=self.normaled.emit)
        layout.addWidget(self._normalButton)
        layout.addWidget(QPushButton(
            "", self, objectName="closeButton", visible=close_visible, clicked=self.closed.emit))


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

        