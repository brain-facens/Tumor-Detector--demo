# imports
from widgets.extras import LoadingIcon, ServerAPI

import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
import PySide6.QtGui as QtG


class Initializer(QtW.QFrame):
    
    def __init__(self, *args, **kargs) -> None:
        super(Initializer, self).__init__(*args, **kargs)
        
        # main variables
        BG_COLOR = '#D9D9D9'
        ICON_COLOR = '#009494'
        
        self.w = 500
        self.h = 300
        
        self.anim_time = 6
        self.counter = 0
        self.done = False
        
        # size
        self.setFixedSize(QtC.QSize(self.w,self.h))
        
        # color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtG.QPalette.ColorRole.Window, QtG.QColor(BG_COLOR))
        self.setPalette(palette)

        # server
        self.server = ServerAPI(route='https://jsonplaceholder.typicode.com/posts') # only test!
        self.server.result_signal.connect(self._request_log)
        
        # layout
        self.brain_logo = QtW.QLabel()
        self.png = QtG.QPixmap('/app/assets/brain.png').scaled(QtC.QSize(130,130))
        self.brain_logo.setPixmap(self.png)
        
        self.title = QtW.QLabel()
        self.title.setText('Tumor Detector')
        self.title.setStyleSheet(f'color: {ICON_COLOR};')
        font = QtG.QFont()
        font.setBold(True)
        font.setPixelSize(15)
        font.setWordSpacing(2)
        self.title.setFont(font)
        
        self.load = LoadingIcon()
        
        self.main_layout = QtW.QVBoxLayout()
        self.main_layout.setAlignment(QtC.Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addWidget(self.brain_logo)
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.load)
        
        self.setLayout(self.main_layout)
        print('Initializing..')
        self._start_request()
    
    def initialization(self) -> bool:
        if self.done:
            print('Initialization Complete!')
            return True
        return False
    
    def _start_request(self) -> None:
        self.server.start()
    
    def _request_log(self, response) -> None:
        print(f'Response status: {response.status_code}')
        self.done = True
