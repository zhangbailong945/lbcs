import ctypes.wintypes
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

GWL_STYLE = -16
HTCLIENT = 1
HTCAPTION = 2    # 标题栏
WM_NCHITTEST = 132
WM_NCCALCSIZE = 131
HTLEFT = 10
HTRIGHT = 11
HTTOP = 12
HTTOPLEFT = 13
HTTOPRIGHT = 14
HTBOTTOM = 15
HTBOTTOMLEFT = 16
HTBOTTOMRIGHT = 17
WM_GETMINMAXINFO = 36
WM_NCLBUTTONDBLCLK = 163  # 鼠标左键双击
WS_THICKFRAME = 262144
WS_CAPTION = 12582912
WS_OVERLAPPED = 0
WS_SYSMENU = 524288
WS_MINIMIZEBOX = 131072
WS_MAXIMIZEBOX = 65536
WS_OVERLAPPEDWINDOW = (WS_OVERLAPPED |
                       WS_CAPTION |
                       WS_SYSMENU |
                       WS_THICKFRAME |
                       WS_MINIMIZEBOX |
                       WS_MAXIMIZEBOX)

class FramelessWindow(QWidget):
    MARGIN_LEFT = 4
    MARGIN_TOP = 4
    MARGIN_RIGHT = 4
    MARGIN_BOTTOM = 4
    TITLE_WIDTH = 144

    def __init__(self, *args, **kwargs):
        super(FramelessWindow, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 如果不加FramelessWindowHint,则可以实现和windows一样的效果,当窗口拖动到边缘会有透明框
        # 但是背景无法透明,如果加上该flag,背景可以透明,但无法实现windows本身窗口动画
        #self.setWindowFlags(Qt.WindowMinimizeButtonHint |Qt.FramelessWindowHint)

        # 这里通过重新设置窗口属性来解决
        style = ctypes.windll.user32.GetWindowLongW(
            int(self.winId()), GWL_STYLE)
        ctypes.windll.user32.SetWindowLongW(
            int(self.winId()), GWL_STYLE, style | WS_MAXIMIZEBOX | WS_THICKFRAME | WS_CAPTION)

        # 这里和nativeEvent中的WM_GETMINMAXINFO近似
        self._setContentsMargins()

    def _setContentsMargins(self):
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.AdjustWindowRectEx(
            ctypes.pointer(rect), WS_OVERLAPPEDWINDOW, False, 0)
        rect.left = abs(rect.left)
        rect.top = abs(rect.bottom)
        self.setContentsMargins(rect.left, rect.top, rect.right, rect.bottom)
        # 鼠标边缘边距
        self.MARGIN_LEFT = abs(rect.left) + 4
        self.MARGIN_TOP = abs(rect.top) + 4
        self.MARGIN_RIGHT = abs(rect.right) + 4
        self.MARGIN_BOTTOM = abs(rect.bottom) + 4

    def GET_Y_LPARAM(self, param):
        return param >> 16

    def GET_X_LPARAM(self, param):
        return param & 0xffff

    def nativeEvent(self, eventType, message):
        if eventType == b"windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            if msg.message == WM_NCCALCSIZE:
                return True, 0
            if msg.message == WM_NCHITTEST:
                xPos = self.GET_X_LPARAM(msg.lParam) - self.frameGeometry().x()
                yPos = self.GET_Y_LPARAM(msg.lParam) - self.frameGeometry().y()
                return self._setResult(xPos, yPos)
#             if msg.message == WM_NCLBUTTONDBLCLK:
#                 if self.isMaximized() or self.isFullScreen():
#                     self.showNormal()
#                 else:
#                     self.showMaximized()
#                 return True, 0
#             if msg.message == WM_GETMINMAXINFO:
#                 if ctypes.windll.user32.IsZoomed(int(self.winId())):
#                     rect = ctypes.wintypes.RECT()
#                     ctypes.windll.user32.AdjustWindowRectEx(ctypes.pointer(rect), WS_OVERLAPPEDWINDOW, False, 0)
#                     rect.left = abs(rect.left)
#                     rect.top = abs(rect.bottom)
#                     self.setContentsMargins(rect.left, rect.top, rect.right, rect.bottom)
#                 return True, 0
        return super(FramelessWindow, self).nativeEvent(eventType, message)

    def _setResult(self, xPos, yPos):
        if self.MARGIN_TOP < yPos <= 36 + self.MARGIN_TOP and xPos < self.width() - self.MARGIN_LEFT - self.TITLE_WIDTH:
            # 标题栏区域
            return True, HTCAPTION
        if self.isMaximized() or self.isFullScreen():
            return True, HTCLIENT
        wm = self.width() - self.MARGIN_LEFT
        hm = self.height() - self.MARGIN_TOP
        if xPos <= self.MARGIN_LEFT and yPos <= self.MARGIN_TOP:
            # 左上角
            return True, HTTOPLEFT
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # 右下角
            return True, HTBOTTOMRIGHT
        elif wm <= xPos and yPos <= self.MARGIN_TOP:
            # 右上角
            return True, HTTOPRIGHT
        elif xPos <= self.MARGIN_LEFT and hm <= yPos:
            # 左下角
            return True, HTBOTTOMLEFT
        elif 0 <= xPos <= self.MARGIN_LEFT and self.MARGIN_TOP <= yPos <= hm:
            # 左边(并且上下各留出self.MARGIN的距离)
            return True, HTLEFT
        elif wm <= xPos <= self.width() and self.MARGIN_TOP <= yPos <= hm:
            # 右边(并且上下各留出self.MARGIN的距离)
            return True, HTRIGHT
        elif self.MARGIN_LEFT <= xPos <= wm and 0 <= yPos <= self.MARGIN_TOP:
            # 上面(并且左右各留出self.MARGIN的距离)
            return True, HTTOP
        elif self.MARGIN_LEFT <= xPos <= wm and hm <= yPos <= self.height():
            # 下面(并且左右各留出self.MARGIN的距离)
            return True, HTBOTTOM
        return True, HTCLIENT

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = FramelessWindow()
    w.setMinimumSize(400, 400)
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec_())
