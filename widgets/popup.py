# imports
from widgets.extras import LoadingIcon

import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
import PySide6.QtGui as QtG


class Initializer(QtW.QFrame):
    
    def __init__(self, *args, **kargs) -> None:
        super(Initializer, self).__init__(*args, **kargs)
        
        # main variables
        BG_COLOR = '#D9D9D9'
        ICON_COLOR = '#0097B2'
        
        self.w = 500
        self.h = 300
        
        self.anim_time = 6
        self.counter = 0
        
        # size
        self.setFixedSize(QtC.QSize(self.w,self.h))
        
        # color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtG.QPalette.ColorRole.Window, QtG.QColor(BG_COLOR))
        self.setPalette(palette)
        
        # layout
        self.brain_logo = QtW.QLabel()
        self.png = QtG.QPixmap('/app/assets/brain.png').scaled(QtC.QSize(130,130))
        self.brain_logo.setPixmap(self.png)
        
        self.title = QtW.QLabel()
        self.title.setText('Tumor Detector')
        self.title.setStyleSheet('color: #009494;')
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
        print('Initializing..', end='\r')
    
    def init_timer(self) -> bool:
        if self.counter == self.anim_time:
            print('Initialization Complete!')
            return True
        self.counter += 1
        return False