
from random import randint

from PyQt5.QtCore import QUrl, QBuffer, QUrlQuery, pyqtSignal, QTimer, Qt
from PyQt5.QtNetwork import QNetworkCookie
from PyQt5.QtWebEngineCore import QWebEngineUrlSchemeHandler,\
    QWebEngineUrlRequestJob
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile,\
    QWebEngineSettings
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar

from Libraries import Config

InjectJs = '''
//document.body.style.background='transparent';
//try{
//    document.getElementsByClassName('create-account-callout')[0].style.background='white';
//}catch(e){}
//添加关闭按钮
//登录页面
var target;
var tabindex = 4;
target = document.getElementsByName('commit')[0];
if(target===undefined) {
    tabindex = 2;
    target = document.getElementsByName('authorize')[0];
}
if(target!==undefined) {
    target = target.parentNode;
    target.innerHTML = target.innerHTML + '<button id="closeWindow" class="btn btn-danger btn-block width-full ws-normal" name="close" tabindex="4" type="button" value="">Close</button>';
    document.getElementById("closeWindow").onclick = function() {
        open("pyqtclient://close", "_self");
    }
}
'''


class UrlSchemeHandler(QWebEngineUrlSchemeHandler):
    '''自定义scheme'''

    codeGeted = pyqtSignal(str)

    def requestStarted(self: QWebEngineUrlSchemeHandler, request: QWebEngineUrlRequestJob) -> None:
        '''
        see: http://doc.qt.io/qt-5/qwebengineurlschemehandler.html#requestStarted
        :param info: see http://doc.qt.io/qt-5/qwebengineurlrequestjob.html
        '''
        # 隐藏浏览器窗口
        self.parent().hide()
        url = request.requestUrl().toString()
        if url.startswith("pyqtclient://close"):
            self._close(request)
            return
        if url.startswith("pyqtclient://login"):
            # 把得到的code返回给其它窗口
            self.codeGeted.emit(
                QUrlQuery(request.requestUrl()).queryItemValue("code"))
            # 关闭窗口(30秒以后，保证cookie被写入,bug)
            QTimer.singleShot(30000, lambda: self._close(request))

    def _close(self, request):
        buffer = QBuffer(self)
        buffer.setData(
            b"<html><head><script>window.close();</script></head></html>")
        request.reply(b"text/html", buffer)
        self.parent().close()


class WebWidget(QWebEngineView):

    _instance = None
    _cookies = []
    closed = pyqtSignal()
    codeGeted = pyqtSignal(str)

    def instance(self, parent: QWidget=None)->QWebEngineView:
        if not WebWidget._instance:
            WebWidget._instance = WebWidget(parent)
        return WebWidget._instance

    def __init__(self, *args, **kwargs):
        super(WebWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        profile = self.page().profile()
        # 去掉滚动条,ShowScrollBars=25,为5.10新增
        self.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        # 设置缓存以及储存路径
        profile.setCachePath(Config.CachePath)
        profile.setPersistentStoragePath(Config.StoragePath)
        profile.setPersistentCookiesPolicy(
            QWebEngineProfile.ForcePersistentCookies)
        # 清理缓存
        profile.clearHttpCache()
        # 清理浏览记录
        profile.clearAllVisitedLinks()
        # 绑定cookie被添加的信号槽
#         profile.cookieStore().cookieAdded.connect(self.onCookieAdd)
        # 安装自定义的url scheme
        url_handler = UrlSchemeHandler(self)
        url_handler.codeGeted.connect(self.codeGeted.emit)
        profile.installUrlSchemeHandler(b"pyqtclient", url_handler)
        # 绑定page的关闭事件,可以通过window.close()触发
        self.page().windowCloseRequested.connect(self.close)
        # 加载完成事件
        self.loadFinished.connect(self.onLoadFinished)

    def load(self, url: str)->None:
        super(WebWidget, self).load(QUrl(url))

    def closeEvent(self, event)->None:
        super(WebWidget, self).closeEvent(event)
        self.closed.emit()

    def clearCookies(self)->None:
        '''
        clear all cookies
        '''
        cookieStore = self.page().profile().cookieStore()
        cookieStore.deleteAllCookies()
        cookieStore.deleteSessionCookies()

    def onCookieAdd(self, cookie: QNetworkCookie)->None:
        self._cookies.append(cookie)

    def onLoadFinished(self, _=None):
        self.page().runJavaScript(InjectJs)

    @classmethod
    def initDevPort(cls):
        while 1:
            port = randint(10000, 65534)
            print("port", port)
            if not os.popen("netstat -an | findstr :" + str(port)).readlines():
                break
        print("dev port:", port)
        os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = str(port)


class WebWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(WebWindow, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self._progressbar = QProgressBar(self, visible=False)
        self._webview = WebWidget(self)
        layout.addWidget(self._progressbar)
        layout.addWidget(self._webview)
        self._webview.closed.connect(self.close)
        self._webview.loadStarted.connect(self.onLoadStarted)
        self._webview.loadFinished.connect(self.onLoadFinished)
        self._webview.loadProgress.connect(self._progressbar.setValue)

    def onLoadStarted(self):
        self._progressbar.setVisible(True)
        self._progressbar.setValue(0)

    def onLoadFinished(self):
        self._progressbar.setValue(100)
        self._progressbar.setVisible(False)


class OAuthWindow(WebWindow):

    def __init__(self, *args, **kwargs):
        super(OAuthWindow, self).__init__(*args, **kwargs)
        self.setMaximumSize(500, 860)
        self.setMinimumSize(500, 860)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setContextMenuPolicy(Qt.NoContextMenu)  # 去掉右键菜单
        self.setWindowModality(Qt.WindowModal)

        self._webview.clearCookies()
        self._webview.load(Config.LoginUrl)
        self._webview.codeGeted.connect(lambda x: print("code:", x))


if __name__ == "__main__":
    import sys
    import os
    os.chdir("../../")
    from PyQt5.QtWidgets import QApplication
    Config.CachePath = "tmp/tmp/cache"
    Config.StoragePath = "tmp/tmp/storage"
    app=QApplication(sys.argv)
    app.setStyleSheet(open("themes/default/qss/default.qss","rb").read().decode("utf-8"))
    WebWidget.initDevPort()
    w = OAuthWindow()
    w.show()
    sys.exit(app.exec_())
