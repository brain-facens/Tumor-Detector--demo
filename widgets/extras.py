# imports
import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
import PySide6.QtGui as QtG

import requests


class LoadingIcon(QtW.QLabel):
    
    def __init__(self, *args, **kargs) -> None:
        super(LoadingIcon, self).__init__(*args, **kargs)

        # main variables
        ICON_COLOR = '#009494'

        self.color = QtG.QColor(ICON_COLOR)

        self.w = 100
        self.h = 80

        # size
        self.setFixedSize(QtC.QSize(self.w, self.h))

        # animator
        self.anim = QtC.QVariantAnimation(self)
        self.anim.setDuration(2000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(360)
        self.anim.valueChanged.connect(self.update)
        self.anim.finished.connect(self._restartAnimation)
        self.anim.start()
    
    def paintEvent(self, arg__1: QtG.QPaintEvent) -> None:
        
        # initializing painter
        painter = QtG.QPainter(self)
        if not painter.isActive():
            painter.begin(self)
        painter.setRenderHint(QtG.QPainter.RenderHint.Antialiasing)

        # defining pen
        pen = QtG.QPen()
        pen.setBrush(QtG.QColor(self.color))
        pen.setWidth(5)
        painter.setPen(pen)

        value = self.anim.currentValue() - 180
        painter.drawArc(35, 5, 60, 60, value * 16, value * 32)

        painter.end()
    
    def _restartAnimation(self):
        self.anim.start()


class ServerAPI(QtC.QThread):

    result_signal = QtC.Signal(requests.Response)

    def __init__(
        self, 
        route: str = '', 
        rbody: dict = None, 
        *args, 
        **kargs
        ) -> None:
        super(ServerAPI, self).__init__(*args, **kargs)

        # main variables
        self.base_url = ''
        self.url = f'{self.base_url}{route}'

        self.body = rbody
    
    def run(self) -> None:
        
        if self.body:
            response = requests.post(url=self.url, json=self.body)
        else:
            response = requests.get(url=self.url)
        self.result_signal.emit(response)
