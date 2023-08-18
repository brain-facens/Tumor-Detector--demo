# imports
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedLayout, QFrame, QHBoxLayout
from PySide6.QtGui import Qt, QPalette, QColor
from PySide6.QtCore import QTimer

from widgets.screen import MainScreen
from widgets.popup import Initializer

import sys


class TumorDetectorDemo(QMainWindow):
    
    def __init__(
        self, 
        *args, 
        **kargs
        ) -> None:
        super(TumorDetectorDemo, self).__init__(*args, **kargs)
        
        # main variables
        BORDER_COLOR = '#A6A6A6'
        BORDER_THICKNESS = 3
        
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self._center_screen()
        
        # multi windows
        self.stk_layout = QStackedLayout()
        for frame in (Initializer(), MainScreen(root=self)):
            self.stk_layout.addWidget(frame)
        self.setFixedSize(self.stk_layout.currentWidget().size())
        
        self.stk_frame = QFrame()
        self.stk_frame.setLayout(self.stk_layout)
        
        # base window
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(BORDER_THICKNESS, BORDER_THICKNESS, BORDER_THICKNESS, BORDER_THICKNESS)
        self.main_layout.setSpacing(0)
        
        self.main_layout.addWidget(self.stk_frame)
        
        self.main_frame = QFrame()
        self.main_frame.setLayout(self.main_layout)
        
        window_border = self.palette()
        window_border.setColor(QPalette.ColorRole.Window, QColor(BORDER_COLOR))
        self.setPalette(window_border)
        
        self.setCentralWidget(self.main_frame)
        
        # timer
        self._initialization_process = QTimer(self)
        self._initialization_process.timeout.connect(self._update_screen)
        self._initialization_process.start(500)

        # displaying window
        self.show()
    
    def _update_screen(self) -> None:
        if self.stk_layout.currentWidget().initialization():
            self.stk_layout.setCurrentIndex(1)
            self.setFixedSize(self.stk_layout.currentWidget().size())
            self._center_screen()
            self._initialization_process.stop()
    
    def _center_screen(self) -> None:
        screen_geometry = self.screen().availableGeometry()
        self._x = (screen_geometry.width() - self.width()) // 2
        self._y = (screen_geometry.height() - self.height()) // 2
        self.move(self._x, self._y)

if __name__=='__main__':
    
    app = QApplication()
    demo = TumorDetectorDemo()
    sys.exit(app.exec())
