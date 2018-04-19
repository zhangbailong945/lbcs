import sys
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Web(QWebEngineView):
    def __init__(self,*args,**kwargs):
        super(Web,self).__init__(*args,**kwargs)

if __name__=="__main__":
    app=QApplication(sys.argv)
    web=Web()
    web.load(QUrl("http://wwww.zhangbailong.com"))
    web.show()
    sys.exit(app.exec_())
