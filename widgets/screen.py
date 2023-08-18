# imports
from widgets.button import MenuButton

import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
import PySide6.QtGui as QtG


class MainScreen(QtW.QFrame):
    
    def __init__(self, root: QtW.QWidget, *args, **kargs) -> None:
        super(MainScreen, self).__init__(*args, **kargs)
        
        # main variables
        self.w = 1200
        self.h = 750
        hmenu = int(self.h * 0.05)
        
        # size
        self.setFixedSize(QtC.QSize(self.w,self.h))
        
        # layout
        self.main_layout = QtW.QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)
        
        self.main_layout.addWidget(MenuBar(root=root, width=self.w, height=hmenu))
        self.main_layout.addWidget(CentralFrame(width=self.w, height=self.h - hmenu))
        
        self.setLayout(self.main_layout)


class MenuBar(QtW.QFrame):
    
    def __init__(
        self, root: QtW.QWidget, 
        width: int, 
        height: int, 
        *args, 
        **kargs
        ) -> None:
        super(MenuBar, self).__init__(*args, **kargs)
        
        # main variables
        BG_COLOR = '#D9D9D9'
        ICON_COLOR = ''
        
        self.dragging = False
        self.offset = None
        self.root = root
        
        # size
        self.setFixedSize(QtC.QSize(width,height))
        
        # color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtG.QPalette.ColorRole.Window, QtG.QColor(BG_COLOR))
        self.setPalette(palette)
        
        # buttons
        self.exit_button = MenuButton(root=root, btype='exit')
        self.exit_button.move(width - 20, self.exit_button.pos().y())
        
        # layout
        self.main_layout = QtW.QHBoxLayout()
        self.main_layout.setAlignment(QtC.Qt.AlignmentFlag.AlignRight)
        self.main_layout.setContentsMargins(1,1,15,1)
        
        self.main_layout.addWidget(self.exit_button)
        
        self.setLayout(self.main_layout)
    
    def mousePressEvent(self, event: QtG.QMouseEvent) -> None:
        if event.button() == QtC.Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.root.pos()
    
    def mouseMoveEvent(self, event: QtG.QMouseEvent) -> None:
        if self.dragging:
            new_pos = event.globalPos() - self.offset
            self.root.move(new_pos)

    def mouseReleaseEvent(self, event: QtG.QMouseEvent) -> None:
        if event.button() == QtC.Qt.MouseButton.LeftButton:
            self.dragging = False


class CentralFrame(QtW.QFrame):
    
    def __init__(
        self,
        width: int, 
        height: int,  
        *args, 
        **kargs
        ) -> None:
        super(CentralFrame, self).__init__(*args, **kargs)
        
        # main variables
        BG_COLOR = '#D9D9D9'
        
        # size
        self.setFixedSize(QtC.QSize(width,height))
        
        # color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtG.QPalette.ColorRole.Window, QtG.QColor(BG_COLOR))
        self.setPalette(palette)
