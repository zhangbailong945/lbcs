from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QProgressBar, QVBoxLayout


class ContentWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(ContentWidget, self).__init__(*args, **kwargs)
        # 保证qss有效
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.initUI()

    def initUI(self):
        '''进度条'''
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self._progressBar = QProgressBar(self, textVisible=False)
        layout.addWidget(self._progressBar)


if __name__ == "__main__":
    import sys
    import os
    os.chdir("../../")
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFontDatabase
    app=QApplication(sys.argv)
    QFontDatabase.addApplicationFont("themes/default/fonts/default.ttf")
    app.setStyleSheet(open("themes/default/qss/default.qss","rb").read().decode("utf-8"))
    w = ContentWidget()
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec_())