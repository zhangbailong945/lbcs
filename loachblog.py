import sys
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication

from Libraries.Widgets.MainWidget import MainWindow

__Author__="LoachBlog"
__Copyright="Copyright©2018 LoachBlog"
__Version__="1.0"

if __name__=="__main__":
    app=QApplication(sys.argv)
    QFontDatabase.addApplicationFont("themes/default/fonts/default.ttf")
    app.setStyleSheet(open("themes/default/qss/default.qss","rb").read().decode("utf-8"))
    w=MainWindow()
    w.show()
    sys.exit(app.exec_())